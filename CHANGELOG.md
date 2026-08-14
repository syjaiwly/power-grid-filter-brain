# Changelog

## [v1.7] - 2026-08-14

### Added
- DC-link voltage constraint for the APF inverter stage.
- L/R interface model using `L di/dt = v_inv - v_grid - R i`.
- Conservative modulation voltage limit and APF current saturation.
- Feed-forward voltage requirement calculation for current-reference tracking.

### Engineering significance
The APF reference is no longer treated as an ideal current source. The controller must now respect available DC-link voltage, interface inductance, resistance and current limits.

### Limitation
This is an averaged control-development plant. Device-level PWM switching, DC-link capacitor energy dynamics, LCL resonance, sampling/computation delay and semiconductor losses remain for subsequent versions.

## [v1.6] - 2026-08-14

### Added
- Reduced-order three-phase APF power-stage model with finite current-loop bandwidth.
- Explicit APF compensation-current reference generator.
- Current-limit behavior in the power-stage model.
- Closed-loop regression test proving harmonic-residual reduction with finite actuator dynamics.

### Architecture
The project is now structured as an APF control brain: observation -> compensation reference -> current-loop/power-stage -> compensated grid response.

### Important limitation
The v1.6 plant is a control-development model, not a transistor-level inverter simulation. PWM, DC-link dynamics, L/LCL filter, sampling delay and semiconductor switching are still to be modeled.

## [v1.5] - 2026-08-14

### Added
- Explicit APF control-brain layer.
- Compensation-current reference generator: APF injects the negative non-fundamental residual.
- Ideal cancellation reference experiment.

### Architecture correction
The project is explicitly an APF control-algorithm brain, not merely a waveform software filter.

## [v1.4] - 2026-08-14

- Added adaptive causal fundamental tracking.

## [v1.3] - 2026-08-14

- Added causal fundamental-state change detector.

## [v1.2] - 2026-08-14

- Added explicit causal tracker latency metric.

## [v1.1] - 2026-08-14

- Added causal fundamental estimator.

## [v1.0] - 2026-08-14

- Added repeatable benchmark harness.

## [v0.9] - 2026-08-14

- Added rectifier ripple, switching transient, load step and composite stress scenarios.

## [v0.8] - 2026-08-14

- Added sag/swell/interruption and interharmonic scenarios.

## [v0.7] - 2026-08-14

- Added symmetrical-component analysis.

## [v0.6-baseline] - 2026-08-14

- Established fixed 50 Hz / 380 V priors and real-time fundamental state estimation.
