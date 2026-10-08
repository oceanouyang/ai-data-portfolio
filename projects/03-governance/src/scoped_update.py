"""In-memory scoped update demonstration, not a durable transaction engine."""
from hashlib import sha256
from pathlib import PurePosixPath
import json


def digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


def apply(current, changes, allowed, baseline, validator):
    for path in changes:
        parsed = PurePosixPath(path)
        if path not in allowed or parsed.is_absolute() or ".." in parsed.parts or "\\" in path:
            raise ValueError("scope_violation")
        if digest(current.get(path, "")) != baseline[path]:
            raise ValueError("target_drift")
    snapshot = dict(current)
    try:
        current.update(changes)
        if not validator(current):
            raise ValueError("validation_failure")
    except Exception:
        current.clear()
        current.update(snapshot)
        raise


if __name__ == "__main__":
    files = {"reports/demo.md": "old", "protected/source.md": "keep"}
    allowed = {"reports/demo.md"}
    baseline = {"reports/demo.md": digest("old")}
    for changes, expected in [({"protected/source.md": "bad"}, "scope_violation"), ({"reports/demo.md": "invalid"}, "validation_failure")]:
        before = dict(files)
        try:
            apply(files, changes, allowed, baseline, lambda state: state["reports/demo.md"] != "invalid")
        except ValueError as error:
            assert str(error) == expected and files == before
        else:
            raise AssertionError("update unexpectedly accepted")
    apply(files, {"reports/demo.md": "new"}, allowed, baseline, lambda _: True)
    try:
        apply(files, {"reports/demo.md": "stale"}, allowed, baseline, lambda _: True)
    except ValueError as error:
        assert str(error) == "target_drift" and files["reports/demo.md"] == "new"
    else:
        raise AssertionError("drift unexpectedly accepted")
    assert files["protected/source.md"] == "keep"
    print(json.dumps({"synthetic": True, "checks": "scope rejection; rollback; selected update; drift rejection", "disk_writes": 0}))
