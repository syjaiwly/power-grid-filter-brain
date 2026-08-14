# Changelog

## [v1.0] - 2026-08-14

### Added
- Repeatable benchmark harness for algorithm comparison.
- RMSE, SNR, THD and runtime metrics in a common result schema.
- Improvement calculations for comparing filter brains.

### Engineering rule
No algorithm optimization is accepted without a repeatable benchmark scenario and regression coverage.

## [v0.9] - 2026-08-14

### Added
- Rectifier/DC-link ripple model (300 Hz default).
- Damped switching-transient model.
- Fundamental load-step model preserving 50 Hz.
- Composite stress scenario combining harmonics, interharmonics, ripple, switching events, load change, voltage events and noise.
- Regression coverage for new disturbance sources.

### Fixed
- Phase-local voltage events now modify the intended phase directly; no advanced-indexing copy bug.

## [v0.8] - 2026-08-14

### Added
- Reusable power-quality event scenario engine.
- Three-phase sag, swell, and interruption events.
- Phase-local or three-phase events.
- Non-integer interharmonic injection.
- Deterministic composite stress scenario.

## [v0.7] - 2026-08-14

### Added
- Positive / negative / zero sequence decomposition.
- Phase-specific harmonic distortion and per-phase DC offset simulation.

### Fixed
- Fundamental phase estimates now use absolute time across sliding windows.

## [v0.6-baseline] - 2026-08-14

### Added
- Fixed 50 Hz grid prior.
- 380 V nominal line-to-line grid model.
- Three-phase fundamental amplitude and phase estimation.
- Sliding-window 50 Hz fundamental reconstruction.
- Harmonic/noise injection and evaluation metrics.
