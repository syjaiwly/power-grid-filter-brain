# Power Grid Filter Brain

三相 50 Hz / 380 V 电网污染数字孪生与滤波算法验证项目。

## 当前版本：v0.7

固定系统先验：
- 电网频率：50 Hz
- 三相线电压额定值：380 V
- 平衡相电压参考：220 V RMS

实时检测变量：
- 三相基波 RMS 幅值
- 三相基波相位
- 三相基波相量
- 正序 / 负序 / 零序状态

核心原则：380 V 是额定系统规格，不把瞬时基波幅值强行固定为 220 V；算法从污染波形中估计真实基波状态，再重构基波。

## 当前数据流

Ideal Grid -> Pollution Models -> Polluted Input
-> 50 Hz Fundamental State Estimator
-> Fundamental Reconstruction
-> Symmetrical Components
-> Evaluation

## 当前污染模型

- 多次谐波
- 三相独立谐波幅值 / 相位 / 比例
- 白噪声
- 每相 DC Offset

更多真实场景（暂降、暂升、间谐波、开关瞬态、整流负载、PWM 等）进入后续场景库，不在当前版本中假装已经完成。

## 研发流程

设计 -> 实现 -> 仿真 -> 测试 -> 评估 -> 优化 -> Git 版本记录

GitHub Actions 已配置为每次 push / pull request 自动运行 pytest。

## 下一步

v0.8：建立真实电网污染场景库，并加入暂降/暂升、间谐波、瞬态、三相不平衡和负载突变的组合测试；随后再比较不同滤波/估计算法的延迟、THD、RMSE 和基波保真度。
