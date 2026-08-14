# Power Grid Filter Brain

三相 50 Hz / 380 V 电网污染数字孪生与滤波算法验证项目。

## 当前版本：v1.1

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

## 当前算法路径

### Offline reference
`Fundamental50HzBrain`
- 滑动窗口最小二乘
- 用于高精度离线重构与算法对照
- 非严格因果，不作为最终实时部署假设

### Real-time candidate
`CausalFundamental50HzBrain`
- 50 Hz 固定先验
- 同步 I/Q 解调
- 指数状态跟踪
- 当前样本只依赖当前及历史样本
- 可调跟踪速度 / 噪声抑制权衡

## 当前数据流

Ideal Grid -> Pollution Models -> Stress Scenario Engine -> Polluted Input
-> Fundamental State Estimator -> Fundamental Reconstruction -> Sequence Analysis -> Benchmark

## 当前污染 / 事件模型

- 多次谐波
- 三相独立谐波幅值 / 相位 / 比例
- 白噪声
- 每相 DC Offset
- 三相或单相暂降 / 暂升 / 中断
- 间谐波
- 300 Hz 整流/DC-link ripple
- 阻尼开关瞬态
- 基波负载突变
- 组合压力场景

## Benchmark

统一记录：
- RMSE
- SNR
- THD
- runtime
- RMSE reduction / SNR gain / THD reduction

后续所有算法优化必须使用同一确定性压力场景进行回归比较。

## 研发流程

设计 -> 实现 -> 仿真 -> 测试 -> 评估 -> 优化 -> Git 版本记录

## 下一步：v1.2

重点转向实时算法工程化：跟踪延迟、状态置信度、突变检测、抗暂态能力，以及不同 `time_constant_cycles` 下的统一 benchmark。
