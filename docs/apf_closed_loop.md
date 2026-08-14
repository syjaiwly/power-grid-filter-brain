# APF closed-loop development model

v1.6 moves the project from waveform reconstruction toward an APF control loop.

```text
Measured 3-phase load current
        -> fundamental state estimator
        -> non-fundamental residual
        -> negative compensation-current reference
        -> current-loop / APF power-stage model
        -> compensated grid current
```

The v1.6 power stage is deliberately reduced-order: a first-order three-phase current-loop plant with an explicit bandwidth and current limit. It is a controller-development model, not a transistor-level inverter simulation.

## Why this layer exists

Before adding PWM, DC-link dynamics, L/LCL filter parameters and semiconductor switching, we need to verify that the algorithm produces the correct compensation direction and that finite current-loop bandwidth does not destroy the expected compensation behavior.

## Next power-stage layers

1. DC-link voltage dynamics and energy balance
2. L/LCL interface model
3. PWM / switching-frequency model
4. Current controller (dq or stationary-frame PR)
5. Sampling and computation delay
6. Current limiting / saturation recovery
7. Grid impedance and weak-grid scenarios
8. Three-phase unbalance and positive/negative/zero-sequence compensation
