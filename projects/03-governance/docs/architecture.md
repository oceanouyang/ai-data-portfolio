# 结构与接口

原阶段成果：来源注册、事务保护与范围检查实现。公开骨架：内存事务与冲突保护。

```text
03-governance/
  README.md
  src/scoped_update.py
  docs/architecture.md
  docs/checks.md
  assets/governance.png
```

流程：预览基线 → 允许目标 → 变更验证 → 提交或恢复。

`src/` 是本轮依据已审阅方法独立重写的可运行安全骨架，使用合成输入，仅依赖 Python 标准库。并非原工程的完整源码，不读取研究数据、不连接网络、不运行模型。

原工具具有磁盘快照与同步流程；此骨架不覆盖生产并发或崩溃恢复。

源码保留输入、核心处理、异常边界和自检入口，便于审核实现规则。具体输出与检查见[回执](checks.md)。

[代码](../src/scoped_update.py) · [项目说明](../README.md)
