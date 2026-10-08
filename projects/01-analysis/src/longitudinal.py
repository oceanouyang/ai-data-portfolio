"""Independent synthetic example; no original research data or result."""
import json
import random
from statistics import mean, pstdev


def prepare(seed=17):
    rng = random.Random(seed)
    rows = []
    for person in range(60):
        intercept, trend = rng.uniform(-1, 1), rng.uniform(-0.1, 0.1)
        for week in range(1, 11):
            rows.append((person, week, intercept + trend * week + rng.gauss(0, 0.12)))
    features = {}
    for person in range(60):
        past = [(w, v) for p, w, v in rows if p == person and w <= 6]
        center_w, center_v = mean(w for w, _ in past), mean(v for _, v in past)
        slope = sum((w - center_w) * (v - center_v) for w, v in past) / sum((w - center_w) ** 2 for w, _ in past)
        features[person] = (center_v, slope)
    people = list(features)
    random.Random(seed + 1).shuffle(people)
    train, valid = people[:45], people[45:]
    centers = [mean(features[p][j] for p in train) for j in range(2)]
    scales = [pstdev(features[p][j] for p in train) for j in range(2)]
    transformed = {p: tuple((features[p][j] - centers[j]) / scales[j] for j in range(2)) for p in people}
    return rows, train, valid, transformed, centers


if __name__ == "__main__":
    rows, train, valid, transformed, centers = prepare()
    assert not set(train) & set(valid)
    assert all(abs(mean(transformed[p][j] for p in train)) < 1e-10 for j in range(2))
    assert prepare()[1:] == (train, valid, transformed, centers)
    # This checks preparation only, not model selection or predictive validity.
    print(json.dumps({"synthetic": True, "people": 60, "feature_cutoff": 6, "train": len(train), "validation": len(valid), "checks": "disjoint people; train-only scaling; reproducible"}))
