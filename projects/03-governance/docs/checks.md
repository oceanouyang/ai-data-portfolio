# 安全骨架检查

本轮独立重写的合成示例已在隔离目录运行，退出码 0，未写入文件。以下是实际运行输出，只支持该示例机制，不代表原工程全面通过。

```json
{
  "synthetic": true,
  "checks": "scope rejection; rollback; selected update; drift rejection",
  "disk_writes": 0
}
```

[代码](../src/scoped_update.py) · [项目说明](../README.md)
