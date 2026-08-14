"""Reusable synthetic power-quality scenarios for algorithm stress testing."""
from dataclasses import dataclass
import numpy as np


@dataclass
class Event:
    start_s: float
    end_s: float
    kind: str
    magnitude: float
    phase: int | None = None


def _mask(t, start, end):
    return (t >= start) & (t < end)


def apply_voltage_events(signal, t, events: list[Event]):
    """Apply physically interpretable voltage events to a 3-phase waveform.

    magnitude is a multiplier for sag/swell, zero for interruption, and is
    phase-local when Event.phase is 0/1/2. The function does not alter the
    nominal grid frequency.
    """
    x = np.asarray(signal, dtype=float).copy()
    if x.ndim != 2 or x.shape[0] != 3:
        raise ValueError("signal must have shape [3, samples]")
    for event in events:
        if event.end_s <= event.start_s:
            raise ValueError("event end_s must be greater than start_s")
        mask = _mask(t, event.start_s, event.end_s)
        phases = range(3) if event.phase is None else [event.phase]
        if event.phase is not None and event.phase not in (0, 1, 2):
            raise ValueError("phase must be 0, 1, 2 or None")
        if event.kind == "sag":
            x[list(phases)][:, mask] *= float(event.magnitude)
        elif event.kind == "swell":
            x[list(phases)][:, mask] *= float(event.magnitude)
        elif event.kind == "interruption":
            x[list(phases)][:, mask] = 0.0
        else:
            raise ValueError(f"unsupported event kind: {event.kind}")
    return x


def add_interharmonic(signal, t, frequency_hz, relative_amplitude, phase_rad=0.0, phase_scales=None):
    """Inject a non-integer-frequency component; useful for converter/load tests."""
    x = np.asarray(signal, dtype=float).copy()
    if x.ndim != 2 or x.shape[0] != 3:
        raise ValueError("signal must have shape [3, samples]")
    rms = np.sqrt(np.mean(x * x, axis=1))
    scales = np.ones(3) if phase_scales is None else np.asarray(phase_scales, dtype=float)
    if scales.shape != (3,):
        raise ValueError("phase_scales must have length 3")
    amp_peak = np.sqrt(2.0) * rms * float(relative_amplitude) * scales
    x += amp_peak[:, None] * np.sin(2*np.pi*frequency_hz*t[None, :] + phase_rad)
    return x


def composite_stress(signal, t, fundamental_hz=50.0, seed=7):
    """Deterministic high-stress scenario used for regression tests."""
    from .pollution import PollutionConfig, Harmonic, inject_pollution
    rng = np.random.default_rng(seed)
    cfg = PollutionConfig(
        harmonics=[
            Harmonic(3, 0.035, [0.1, -0.3, 0.2], [1.0, 0.8, 1.2]),
            Harmonic(5, 0.045, [-0.2, 0.4, -0.1], [1.1, 0.9, 1.0]),
            Harmonic(7, 0.025, [0.5, -0.2, 0.3], [0.9, 1.2, 0.8]),
            Harmonic(11, 0.015, [0.0, 0.7, -0.5], [1.0, 0.8, 1.1]),
        ],
        noise_rms_v=0.7,
        dc_offset_v=[0.5, -0.3, 0.2],
        seed=seed,
    )
    polluted = inject_pollution(signal, fundamental_hz, t, cfg)
    polluted = add_interharmonic(polluted, t, 83.0, 0.012, phase_rad=0.2,
                                 phase_scales=[1.0, 0.7, 1.25])
    events = [
        Event(0.07, 0.095, "sag", 0.82, phase=None),
        Event(0.13, 0.145, "swell", 1.10, phase=1),
        Event(0.18, 0.185, "interruption", 0.0, phase=2),
    ]
    polluted = apply_voltage_events(polluted, t, events)
    polluted += rng.normal(0.0, 0.05, size=polluted.shape)
    return polluted, events
