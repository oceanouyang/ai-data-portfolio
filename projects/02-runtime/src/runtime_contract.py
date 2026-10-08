"""Pure synthetic contract checks. Does not connect to an engine."""
from dataclasses import dataclass, replace
import json


@dataclass(frozen=True)
class Snapshot:
    ready: bool
    active_model: str
    expected_model: str
    input_tokens: int
    output_budget: int
    context: int
    kv_total: int
    concurrency: int
    free_mib: int
    min_free_mib: int


def check(s):
    counts = (s.input_tokens, s.output_budget, s.context, s.kv_total, s.free_mib, s.min_free_mib)
    if any(v < 0 for v in counts) or s.concurrency < 1 or s.context < 1:
        return ["invalid_capacity"]
    errors = []
    if not s.ready:
        errors.append("backend_unavailable")
    if s.active_model != s.expected_model:
        errors.append("model_mismatch")
    if s.input_tokens + s.output_budget > s.context:
        errors.append("context_overflow")
    if s.context * s.concurrency > s.kv_total:
        errors.append("shared_kv_overcommit")
    if s.free_mib < s.min_free_mib:
        errors.append("insufficient_headroom")
    return errors


if __name__ == "__main__":
    sample = Snapshot(True, "model-demo", "model-demo", 7000, 1000, 8192, 8192, 1, 2200, 1500)
    assert check(sample) == []
    changes = [("ready", False, "backend_unavailable"), ("active_model", "other", "model_mismatch"), ("output_budget", 2000, "context_overflow"), ("concurrency", 2, "shared_kv_overcommit"), ("free_mib", 1400, "insufficient_headroom")]
    for field, value, expected in changes:
        assert expected in check(replace(sample, **{field: value}))
    print(json.dumps({"synthetic": True, "checks": 6, "scope": "capacity contract only; no engine measurement"}))
