# 结构与接口

原阶段成果：论文中的 DTS、FRQ、RC 与传统评测工具。公开骨架：三种传统策略、频率修正对照与配对区间。

```text
04-hangman/
  README.md
  src/hangman_fairness.py
  docs/architecture.md
  docs/checks.md
  assets/hangman.png
```

流程：已知词长 → 位置字母询问 → 信息增益 → 候选更新。

`src/` 是本轮依据已审阅方法独立重写的可运行安全骨架，使用合成输入，仅依赖 Python 标准库。并非原工程的完整源码，不读取研究数据、不连接网络、不运行模型。

论文工具包含 GUI、随机与词长分层采样、配对统计和样本量稳定实验；骨架仅用合成词集与逐词配对 Bootstrap，不附原词典或正式成绩。

源码保留输入、核心处理、异常边界和自检入口，便于审核实现规则。具体输出与检查见[回执](checks.md)。

[代码](../src/hangman_fairness.py) · [项目说明](../README.md)
