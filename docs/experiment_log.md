# Experiment Log

## Baseline experiment

Scenario:
- 50 Hz fixed
- 380 V line-to-line nominal system
- Three-phase waveform
- Harmonic contamination and additive white noise
- Sliding-window 50 Hz fundamental reconstruction

Metrics recorded by the evaluation module:
- Input/output RMSE
- Input/output SNR
- Input/output THD

The experiment harness is intentionally kept separate from the core algorithm so future versions can be compared against the same scenarios.

## Acceptance principle

A filter is not considered successful merely because THD decreases. It must also preserve the legitimate 50 Hz fundamental state, including real amplitude changes, phase changes, unbalance, and transient events.
