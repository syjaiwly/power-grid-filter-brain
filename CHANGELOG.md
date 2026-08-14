# Changelog

## [v1.1] - 2026-08-14

### Added
- CausalFundamental50HzBrain for real-time experiments.
- Synchronous I/Q demodulation with exponential state tracking.
- Explicit separation between offline sliding-window reference and causal deployment candidate.
- Regression tests for amplitude-step tracking and Nyquist validation.

### Engineering rule
A deployment candidate must be causal: its output at sample k may depend only on samples up to k. Offline zero/future-lookahead estimators remain useful as accuracy references.

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

### Fixed
- Phase-local voltage events now modify the intended phase directly.

## [v0.8] - 2026-08-14

- Added sag/swell/interruption and interharmonic scenario engine.

## [v0.7] - 2026-08-14

- Added symmetrical components and stronger state validation.

## [v0.6-baseline] - 2026-08-14

- Fixed 50 Hz prior and real-time fundamental amplitude/phase estimation.
