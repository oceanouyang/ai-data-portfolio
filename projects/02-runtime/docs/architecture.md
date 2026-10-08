# 结构与接口

原阶段成果：历史容量调优与检索验收记录。公开骨架：纯函数运行契约。

```text
02-runtime/
  README.md
  src/runtime_contract.py
  docs/architecture.md
  docs/checks.md
  assets/runtime.png
```

流程：期望身份 / 输入输出预算 → 运行契约 → 拒绝或接纳。

`src/` 是本轮依据已审阅方法独立重写的可运行安全骨架，使用合成输入，仅依赖 Python 标准库。并非原工程的完整源码，不读取研究数据、不连接网络、不运行模型。

原系统包含控制器、路由器和推理引擎；此骨架不连接真实服务。

源码保留输入、核心处理、异常边界和自检入口，便于审核实现规则。具体输出与检查见[回执](checks.md)。

[代码](../src/runtime_contract.py) · [项目说明](../README.md)
