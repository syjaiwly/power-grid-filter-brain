# Changelog

## [v1.3] - 2026-08-14

### Added
- Causal fundamental-state change detector using 50 Hz I/Q phasor comparison.
- Non-overlapping one-cycle comparison to avoid confusing steady-state presence with a change.
- Coherence-gated change confidence.

### Effect demonstrated
- A real 50 Hz amplitude step produced peak change confidence ≈ 0.247 in the reference scenario.
- A pure 5th-harmonic (250 Hz) disturbance produced ≈ 0.000 confidence.
- Decision threshold in the reference scenario: 0.20.

### Engineering rule
The detector is a confidence signal, not an absolute truth classifier. It should protect legitimate fundamental changes from aggressive filtering while handing low-confidence disturbances to the pollution-removal path.

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
