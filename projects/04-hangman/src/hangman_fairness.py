"""Independent toy comparison, position-letter queries with a known lexicon."""
from math import log2
from random import Random
import json


def choose(words, asked, strategy, rng=None):
    if strategy not in {"legacy_frequency", "fair_frequency", "gain", "RC"}:
        raise ValueError("unknown strategy")
    candidates = []
    for position in range(len(words[0])):
        for letter in sorted({w[position] for w in words}):
            question = (position, letter)
            if question in asked:
                continue
            probability = sum(w[position] == letter for w in words) / len(words)
            if strategy in {"fair_frequency", "gain"} and probability in (0, 1):
                continue
            score = probability
            if strategy == "gain":
                score = -probability * log2(probability) - (1 - probability) * log2(1 - probability)
            candidates.append((score, question))
    if not candidates:
        raise ValueError("no discriminating query")
    if strategy == "RC":
        if rng is None:
            raise ValueError("RC needs a local seeded generator")
        return rng.choice(sorted(question for _, question in candidates))
    return sorted(candidates, key=lambda item: (-item[0], item[1]))[0][1]


def solve(dictionary, target, strategy, seed=42):
    words = sorted({w for w in dictionary if len(w) == len(target)})
    if target not in words:
        raise ValueError("target outside lexicon")
    asked, trace, rng = set(), [], Random(seed)
    while len(words) > 1:
        question = choose(words, asked, strategy, rng)
        position, letter = question
        answer = target[position] == letter
        asked.add(question)
        words = [w for w in words if (w[position] == letter) == answer]
        trace.append({"question": question, "remaining": len(words)})
    return words[0], trace


def paired_summary(dts_counts, frq_counts, seed=42, repeats=1000):
    if len(dts_counts) != len(frq_counts) or not dts_counts or repeats < 2:
        raise ValueError("paired observations and at least two resamples required")
    differences = [a - b for a, b in zip(dts_counts, frq_counts)]
    rng = Random(seed)
    means = sorted(sum(rng.choice(differences) for _ in differences) / len(differences) for _ in range(repeats))
    return {"mean_dts_minus_frq": sum(differences) / len(differences),
            "bootstrap_percentile_95": [means[int(.025 * (repeats - 1))], means[int(.975 * (repeats - 1))]],
            "scope": "paired synthetic targets; interval is not thesis significance"}


if __name__ == "__main__":
    toy = ["aaa", "aba"]
    result = {}
    for strategy in ("legacy_frequency", "fair_frequency", "gain"):
        counts = []
        for target in toy:
            identified, trace = solve(toy, target, strategy)
            assert identified == target
            counts.append(len(trace))
        result[strategy] = counts
    assert result == {"legacy_frequency": [3, 3], "fair_frequency": [1, 1], "gain": [1, 1]}
    rc_counts = []
    for target in toy:
        identified, trace = solve(toy, target, "RC")
        assert identified == target and solve(toy, target, "RC") == (identified, trace)
        rc_counts.append(len(trace))
    paired = paired_summary(result['gain'], result['legacy_frequency'])
    assert paired['mean_dts_minus_frq'] == -2 and paired['bootstrap_percentile_95'] == [-2, -2]
    assert solve(["aaa"], "aaa", "gain")[1] == []
    try:
        solve(toy, "abc", "gain")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown target accepted")
    print(json.dumps({"synthetic": True, "guesses_per_target": {"DTS": result['gain'], "FRQ_legacy": result['legacy_frequency'], "FRQ_fair": result['fair_frequency'], "RC_seed42": rc_counts}, "paired_summary": paired, "scope": "toy mechanism only; no benchmark superiority claim"}))
