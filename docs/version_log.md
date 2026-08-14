# Version Log

## v0.7 — 2026-08-14

### Optimized
- Fixed a subtle phase-reference bug: each sliding-window estimate is now referenced to absolute sample time, so phase history is physically comparable between windows.
- Added input validation and explicit Nyquist-rate checks.
- Kept 50 Hz as a fixed system prior; frequency estimation is not performed.

### Added
- Three-phase RMS phasor construction.
- Positive / negative / zero sequence decomposition.
- Sequence-magnitude tests for balanced and unbalanced systems.
- Phase-specific harmonic amplitude/phase/scale in the pollution model.
- Per-phase DC offset injection.

### Engineering rule
380 V is the nominal line-to-line system specification, not a clamp on the reconstructed waveform. The algorithm must preserve legitimate fundamental amplitude changes and unbalance.

## v0.6-baseline — 2026-08-14

- Locked system priors at 50 Hz and 380 V nominal line-to-line.
- Added fixed-frequency 50 Hz fundamental extraction.
- Added real-time estimation of per-phase fundamental RMS amplitude and phase.
- Added sliding-window reconstruction.
- Added harmonic/noise injection and baseline evaluation metrics.
- Added first automated test for amplitude/phase estimation.
