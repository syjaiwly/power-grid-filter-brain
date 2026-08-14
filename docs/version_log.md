# Version Log

## v0.6-baseline — 2026-08-14

- Locked system priors at 50 Hz and 380 V nominal line-to-line.
- Added fixed-frequency 50 Hz fundamental extraction.
- Added real-time estimation of per-phase fundamental RMS amplitude and phase.
- Added sliding-window reconstruction.
- Added harmonic/noise injection and baseline evaluation metrics.
- Added first automated test for amplitude/phase estimation.

### Design correction

Earlier experimentation incorrectly treated the 50 Hz frequency as a variable to estimate. That is not the project requirement. 50 Hz is fixed. The real-time state to estimate is the fundamental electrical state: amplitude, phase, and later three-phase sequence state.

## Next: v0.7

- Phase continuity handling
- Positive/negative/zero sequence decomposition
- Three-phase fundamental state analysis
