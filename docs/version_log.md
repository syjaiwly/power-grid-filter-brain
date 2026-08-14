# Version Log

## v1.0 — 2026-08-14

### Added
- Repeatable benchmark harness with common metrics and runtime measurement.
- Explicit improvement calculations for RMSE, SNR and THD.
- Regression test to keep the benchmark interface stable.

### Engineering rule
Every future algorithm version must be compared against the same deterministic stress scenario before it is considered an improvement.

## v0.9 — 2026-08-14

### Added
- Rectifier/DC-link ripple.
- Damped switching transients.
- Fundamental load-step events.
- Composite stress scenario combining multiple pollution mechanisms.

### Fixed
- Phase-local event mutation bug.

## v0.8 — 2026-08-14

- Added reusable sag/swell/interruption and interharmonic scenario engine.

## v0.7 — 2026-08-14

- Fixed absolute-time phase reference.
- Added symmetrical components and stronger validation.

## v0.6-baseline — 2026-08-14

- Fixed 50 Hz grid prior.
- Added real-time fundamental amplitude/phase estimation and reconstruction.
