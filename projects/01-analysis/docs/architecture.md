# 结构与接口

原阶段成果：冻结分析报告与验证边界。公开骨架：纵向特征准备与泄漏保护。

```text
01-analysis/
  README.md
  src/longitudinal.py
  docs/architecture.md
  docs/checks.md
  assets/analysis.png
```

流程：合成记录 → 时间截止 → 个体划分 → 训练集变换。

`src/` 是本轮依据已审阅方法独立重写的可运行安全骨架，使用合成输入，仅依赖 Python 标准库。并非原工程的完整源码，不读取研究数据、不连接网络、不运行模型。

原分析还包含潜变量、重抽样、外层验证和置换；此骨架仅保留数据准备接口。

源码保留输入、核心处理、异常边界和自检入口，便于审核实现规则。具体输出与检查见[回执](checks.md)。

[代码](../src/longitudinal.py) · [项目说明](../README.md)
