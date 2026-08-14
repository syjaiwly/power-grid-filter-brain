# Version Log

## v1.4 — 2026-08-14

### Added
- AdaptiveCausalFundamental50HzBrain.
- Coherence-based adaptive tracking speed.
- Fast path for sustained 50 Hz-coherent fundamental changes.
- Slow path for incoherent/high-frequency disturbances.
- Regression coverage for a real 50 Hz amplitude step and pure 5th-harmonic rejection.

### Interpretation
The filter no longer treats every instantaneous error as a reason to rewrite the fundamental state. It evaluates whether the innovation is phase-coherent with the fixed 50 Hz reference.

### Limitation
The gate is a causal heuristic. Thresholds and time constants require broad benchmark calibration before any hardware deployment claim.

## v1.3 — 2026-08-14

- Added causal fundamental-state change detector using 50 Hz I/Q phasor comparison.
- Reference test: real 50 Hz amplitude step confidence ≈ 0.247; pure 5th harmonic ≈ 0.000.

## v1.2 — 2026-08-14

- Added explicit causal tracker latency metric and hardened real-time state handling.

## v1.1 — 2026-08-14

- Added CausalFundamental50HzBrain using synchronous I/Q demodulation and exponential tracking.

## v1.0 — 2026-08-14

- Added deterministic benchmark harness and common comparison metrics.

## v0.9 — 2026-08-14

- Added rectifier ripple, switching transients, load steps and composite stress testing.

## v0.8 — 2026-08-14

- Added sag/swell/interruption and interharmonic scenario engine.

## v0.7 — 2026-08-14

- Fixed absolute-time phase reference and added symmetrical components.

## v0.6-baseline — 2026-08-14

- Fixed 50 Hz prior and real-time fundamental amplitude/phase estimation.
