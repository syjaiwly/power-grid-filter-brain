# Changelog

## [v0.8] - 2026-08-14

### Added
- Reusable power-quality event scenario engine.
- Three-phase sag, swell, and interruption events.
- Phase-local or three-phase events.
- Non-integer interharmonic injection.
- Deterministic composite stress scenario combining harmonics, interharmonics, DC offset, noise, sag, swell, and interruption.
- Regression tests for scenario correctness and reproducibility.

### Fixed
- Phase-local voltage event mutation now updates the intended phase instead of a temporary advanced-indexing copy.

### Design rule
Scenario generation must preserve the 50 Hz grid prior while independently stressing amplitude, balance, waveform purity, and transient behavior.

## [v0.7] - 2026-08-14

### Added
- Positive / negative / zero sequence decomposition.
- Phase-specific harmonic distortion and per-phase DC offset simulation.
- Stronger automated tests for balanced and unbalanced three-phase states.

### Fixed
- Fundamental phase estimates now use absolute time across sliding windows.

### Hardened
- Input shape validation.
- Sample-rate / Nyquist validation.

## [v0.6-baseline] - 2026-08-14

### Added
- Fixed 50 Hz grid prior.
- 380 V nominal line-to-line grid model.
- Three-phase fundamental amplitude and phase estimation.
- Sliding-window 50 Hz fundamental reconstruction.
- Harmonic/noise pollution model.
- RMSE, SNR and THD evaluation metrics.
- Baseline automated test.

### Design rule
50 Hz is fixed; the real-time fundamental state is not fixed.
