# Power Grid Filter Brain — APF Control Brain

三相 50 Hz / 380 V 电网污染数字孪生与 APF（有源电力滤波器）控制算法验证项目。

## 系统定位

本项目不是单纯的软件波形滤波器，而是 **APF 的算法大脑**：

```text
污染电网 / 负载电流
        ↓
电网状态观测
        ↓
基波 + 序分量 + 谐波 + 无功 + 不平衡
        ↓
补偿目标计算
        ↓
APF补偿电流参考
        ↓
电流控制 / PWM / 逆变器
        ↓
向电网注入反向补偿
        ↓
净化后的电网电流
```

## 固定系统先验

- 电网频率：50 Hz
- 三相线电压额定值：380 V
- 平衡相电压参考：220 V RMS

这些是系统先验和额定值，不是强制的瞬时基波状态。实际基波 RMS 幅值、相位、三相不平衡状态必须实时估计。

## 当前算法层级

### 1. Fundamental State Estimator

`Fundamental50HzBrain`：离线高精度参考估计。

`CausalFundamental50HzBrain`：严格因果的实时候选算法。

- 50 Hz 固定先验
- I/Q 同步解调
- 实时幅值 / 相位状态跟踪
- 只使用当前及历史采样

### 2. Pollution / State Discriminator

判断当前变化更像真实 50 Hz 基波状态变化还是非基波污染，并控制跟踪速度。

### 3. APF Compensation Reference

`harmonic_compensation_reference()`：测得负载电流减去目标基波，取负号生成 APF 补偿电流参考。

### 4. APF Power Stage — v1.6

`ThreePhaseAPFPowerStage` 是第一版闭环功率级开发模型：

- 三相电流通道
- 有限电流环带宽
- 补偿电流限幅
- 采样级离散仿真

它用于验证算法参考经过有限执行机构后还能否有效降低污染；不是最终的器件级逆变器模型。

## 当前数据流

Ideal Grid → Load / Pollution Digital Twin → Measurement
→ Fundamental State Estimator → Pollution / Sequence Analysis
→ APF Compensation Reference → Current Loop / Power Stage
→ Grid + APF Closed Loop → Evaluation

## 下一阶段

- DC-link 电压与能量动态
- L / LCL 接口模型
- PWM / 开关频率模型
- PR / dq 电流控制器
- 采样与计算延迟
- 限流与饱和恢复
- 电网阻抗 / 弱电网
- 正序 / 负序 / 零序统一补偿
- 无功 + 谐波 + 不平衡统一补偿

## 研发流程

**设计 → 实现 → 仿真 → 测试 → 效果展示 → 评估 → 优化 → Git版本记录**

每次算法修改必须保留可重复实验和前后对比结果。
