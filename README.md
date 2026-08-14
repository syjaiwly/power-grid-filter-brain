# Power Grid Filter Brain

三相 50 Hz / 380 V 电网污染数字孪生与滤波算法验证项目。

## 当前基线：v0.6

固定系统先验：
- 电网频率：50 Hz
- 三相线电压额定值：380 V
- 平衡相电压参考：220 V RMS

实时检测变量：
- 三相基波 RMS 幅值
- 三相基波相位
- 基波状态随时间的变化

核心原则：380 V 是额定系统规格，不把瞬时基波幅值强行固定为 220 V；算法从污染波形中估计真实基波状态，再重构基波。

## 数据流

Ideal Grid -> Pollution Models -> Scenario Engine -> Polluted Input
-> Algorithm Brain -> Clean Fundamental -> Evaluation

## 已覆盖的污染模型

- 3/5/7/11/13 次谐波
- 间谐波
- 白噪声
- Sag / Swell / Interruption
- DC Offset
- Composite Stress Scenario

## 研发流程

设计 -> 实现 -> 仿真 -> 测试 -> 评估 -> 优化 -> Git 版本记录

## 下一版本

v0.7：相位连续化、正序/负序/零序分解、三相状态分析。