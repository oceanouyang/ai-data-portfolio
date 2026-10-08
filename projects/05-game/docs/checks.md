# 安全骨架检查

本轮独立重写的合成示例已在隔离目录运行，退出码 0，未写入文件。以下是实际运行输出，只支持该示例机制，不代表原工程全面通过。

```json
{
  "synthetic": true,
  "craft_once": true,
  "validation_rollback": true,
  "stale_snapshot_rejected": true,
  "layout_checks": 8,
  "scope": "in-memory contract only; no Godot runtime or real saves"
}
```

[代码](../src/game_rules.py) · [项目说明](../README.md)
