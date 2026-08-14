# v2.4 — Nonlinear rectifier stress test

## Purpose

Replace hand-injected 5th/7th harmonics with a reduced-order three-phase diode-bridge + DC-link load. The load naturally creates narrow capacitor-charging current pulses and a broadband harmonic spectrum.

## Test chain

```text
3-phase 380 V / 50 Hz source
        |
        v
 diode bridge
        |
    DC capacitor
        |
      R load
        |
      PCC <---- APF compensation current
```

## What must be measured

- Load-current RMS and residual RMS
- THD before/after APF
- compensation-current peak/RMS
- detection latency after a load step
- 10–90% compensation response time
- DC-link voltage excursion
- current-controller saturation time
- fundamental-amplitude tracking error

## Acceptance gates for v2.4

The project must **measure** these rather than assume them:

1. Response target: total detection + reference-generation latency < 5 ms.
2. Fundamental 50 Hz state must remain trackable when its amplitude changes.
3. APF reference must not command unlimited current; saturation must be explicit.
4. A nonlinear load step must be included, not only stationary harmonics.
5. Results must be reported per phase and as a three-phase aggregate.

## Engineering note

The rectifier model is a reduced-order controller-development model. It is not yet the final switching-level power stage. Device reverse recovery, PWM dead time, parasitic inductance, DC-link ripple, L/LCL filter dynamics and digital computation delay remain part of the next fidelity increment.
