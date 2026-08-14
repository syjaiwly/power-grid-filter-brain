# Version Log

## v1.2 — 2026-08-14

### Added
- Explicit causal tracker latency metric based on the configured 50 Hz state time constant.
- Hardened real-time input/parameter validation.
- Clear deployment rule separating causal state tracking from offline reference reconstruction.

### Key engineering rule
Latency is now a first-class metric. We will not accept an apparent filtering improvement if it relies on future samples or hides unacceptable tracking delay.

## v1.1 — 2026-08-14

### Added
- CausalFundamental50HzBrain using synchronous I/Q demodulation and exponential tracking.
- Explicit causal-vs-offline estimator distinction.
- Regression tests for amplitude-step tracking.

### Key engineering finding
The previous sliding-window estimator is useful as an offline reference but is not strictly causal. A real deployment path therefore needs a causal state tracker.

## v1.0 — 2026-08-14

- Added deterministic benchmark harness and common comparison metrics.

## v0.9 — 2026-08-14

- Added rectifier ripple, switching transients, load steps and composite stress testing.

## v0.8 — 2026-08-14

- Added sag/swell/interruption and interharmonic scenario engine.

## v0.7 — 2026-08-14

- Fixed absolute-time phase reference.
- Added symmetrical components.

## v0.6-baseline — 2026-08-14

- Fixed 50 Hz prior and real-time fundamental amplitude/phase estimation.
