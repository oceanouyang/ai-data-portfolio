# 安全骨架检查

本轮独立重写的合成示例已在隔离目录运行，退出码 0，未写入文件。以下是实际运行输出，只支持该示例机制，不代表原工程全面通过。

```json
{
  "synthetic": true,
  "guesses_per_target": {
    "DTS": [
      1,
      1
    ],
    "FRQ_legacy": [
      3,
      3
    ],
    "FRQ_fair": [
      1,
      1
    ],
    "RC_seed42": [
      2,
      2
    ]
  },
  "paired_summary": {
    "mean_dts_minus_frq": -2.0,
    "bootstrap_percentile_95": [
      -2.0,
      -2.0
    ],
    "scope": "paired synthetic targets; interval is not thesis significance"
  },
  "scope": "toy mechanism only; no benchmark superiority claim"
}
```

[代码](../src/hangman_fairness.py) · [项目说明](../README.md)
