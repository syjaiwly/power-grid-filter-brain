# Changelog

## [v2.0] - 2026-08-14

### Added
- Multi-time-scale pollution detection: 0.5-cycle fast discovery + 1-cycle confirmation.
- Causal fusion rule for APF compensation-reference generation.
- Detection-latency benchmark comparing 0.5, 1 and 2 cycles.
- Fundamental-protection validation: real 50 Hz amplitude changes remain state changes rather than pollution.

### Benchmark
For a 250 Hz pollution step at 20 kHz sampling:
- 0.5-cycle detector: 10-90% = 1.00 ms.
- 1-cycle detector: 10-90% = 2.65 ms.
- 2-cycle detector: 10-90% = 6.25 ms.

### Engineering rule
The fast detector is allowed to discover a change early, but the compensation reference is enabled only after the slower confirmation channel agrees. This separates detection speed from decision confidence.

### Current limitation
The v2.0 fusion is a reference-generation layer. It still requires full three-phase sequence-aware validation, discrete PWM/sampling delay, DC-link dynamics, weak-grid impedance and saturation/recovery stress testing before hardware-oriented claims.

## [v1.8] - 2026-08-14

### Added
- Response-time metrics as a first-class APF acceptance criterion.
- 10-90% rise-time measurement.
- 10% settling-time measurement.
- Overshoot measurement for dynamic compensation tests.
- Explicit engineering requirement: suppression speed must be evaluated together with harmonic attenuation and fundamental preservation.

### Engineering rule
An APF algorithm is not considered better merely because it removes more pollution. It must also respond fast enough to load/harmonic changes while remaining causal and stable.

### Current limitation
The response metrics are now in the software framework, while the next validation step is a discrete PWM + sampling/computation-delay plant with DC-link capacitor dynamics.

## [v1.7] - 2026-08-14

### Added
- DC-link voltage constraint for the APF inverter stage.
- L/R interface model using `L di/dt = v_inv - v_grid - R i`.
- Conservative modulation voltage limit and APF current saturation.
- Feed-forward voltage requirement calculation for current-reference tracking.

### Engineering significance
The APF reference is no longer treated as an ideal current source. The controller must now respect available DC-link voltage, interface inductance, resistance and current limits.

## [v1.6] - 2026-08-14

### Added
- Reduced-order three-phase APF power-stage model with finite current-loop bandwidth.
- Explicit APF compensation-current reference generator.
- Current-limit behavior in the power-stage model.
- Closed-loop regression test proving harmonic-residual reduction with finite actuator dynamics.

## [v1.5] - 2026-08-14

- Added explicit APF control-brain layer and compensation-current reference generator.

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
