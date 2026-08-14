# Architecture

## System specification

- Three-phase AC grid
- Frequency fixed at 50 Hz
- Nominal line-to-line voltage 380 V
- Balanced phase-to-neutral reference 220 V RMS

## Processing pipeline

```text
Grid model
  -> pollution injection
  -> polluted three-phase waveform
  -> fundamental state estimator
  -> 50 Hz fundamental reconstruction
  -> evaluation
```

## Fundamental state

The 50 Hz frequency is a fixed prior. The algorithm estimates, rather than hard-codes:

- RMS amplitude of each phase
- phase angle of each phase
- evolution of those states over time

The nominal 380 V / 220 V values are references, not forced output values. Legitimate voltage changes must remain observable.

## Roadmap

1. Positive/negative/zero sequence decomposition
2. Confidence and transient detection
3. Harmonic/interharmonic separation
4. Broad real-world pollution scenario library
5. Robustness and latency evaluation
