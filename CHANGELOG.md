# Changelog

## [v1.4] - 2026-08-14

### Added
- AdaptiveCausalFundamental50HzBrain.
- Fast tracking when the present/past innovation is coherent with 50 Hz.
- Slow tracking when the disturbance is incoherent/high-frequency.
- Explicit change-confidence state history.
- Regression test for preserving a real 50 Hz amplitude step while rejecting a pure 5th harmonic.

### Engineering effect
The filter now has a decision mechanism before writing a disturbance into the estimated fundamental state: coherent 50 Hz change is allowed through faster; incoherent pollution is suppressed by slower state adaptation.

### Important limitation
This is a causal heuristic, not yet a certified power-quality classifier. Thresholds and time constants must be benchmarked against a much larger scenario matrix before deployment.

## [v1.3] - 2026-08-14

- Added causal fundamental-state change detector using 50 Hz I/Q phasor comparison.
- Real 50 Hz amplitude step: peak confidence ≈ 0.247 in reference scenario; pure 5th harmonic ≈ 0.000.

## [v1.2] - 2026-08-14

- Added explicit causal tracker latency metric and hardened real-time state handling.

## [v1.1] - 2026-08-14

- Added CausalFundamental50HzBrain and causal-vs-offline estimator distinction.

## [v1.0] - 2026-08-14

- Added repeatable benchmark harness and common comparison metrics.

## [v0.9] - 2026-08-14

- Added rectifier ripple, switching transients, load steps and composite stress testing.

## [v0.8] - 2026-08-14

- Added sag/swell/interruption and interharmonic scenario engine.

## [v0.7] - 2026-08-14

- Added symmetrical components and stronger state validation.

## [v0.6-baseline] - 2026-08-14

- Fixed 50 Hz prior and real-time fundamental amplitude/phase estimation.
