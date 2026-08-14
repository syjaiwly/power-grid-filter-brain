# Changelog

## [v1.2] - 2026-08-14

### Added
- Explicit causal tracker latency metric (`time_constant_cycles / 50 Hz`).
- Hardened real-time I/Q tracker validation and state handling.
- Clear separation between offline reference and causal deployment candidate.

### Engineering rule
Real-time output must never depend on future samples. Latency and tracking-speed trade-offs must be measurable rather than hidden inside filter parameters.

## [v1.1] - 2026-08-14

### Added
- CausalFundamental50HzBrain for real-time experiments.
- Synchronous I/Q demodulation with exponential state tracking.
- Explicit separation between offline sliding-window reference and causal deployment candidate.
- Regression tests for amplitude-step tracking and Nyquist validation.

## [v1.0] - 2026-08-14

### Added
- Repeatable benchmark harness for algorithm comparison.
- RMSE, SNR, THD and runtime metrics in a common result schema.
- Improvement calculations for comparing filter brains.

## [v0.9] - 2026-08-14

### Added
- Rectifier/DC-link ripple model.
- Damped switching-transient model.
- Fundamental load-step model preserving 50 Hz.
- Composite stress scenario combining multiple pollution mechanisms.

## [v0.8] - 2026-08-14

- Added sag/swell/interruption and interharmonic scenario engine.

## [v0.7] - 2026-08-14

- Added symmetrical components and stronger state validation.

## [v0.6-baseline] - 2026-08-14

- Fixed 50 Hz prior and real-time fundamental amplitude/phase estimation.
