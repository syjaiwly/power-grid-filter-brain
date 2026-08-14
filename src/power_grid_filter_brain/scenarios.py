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
    """Apply voltage events without changing nominal 50 Hz frequency."""
    x = np.asarray(signal, dtype=float).copy()
    if x.ndim != 2 or x.shape[0] != 3 or len(t) != x.shape[1]:
        raise ValueError("signal must have shape [3, samples] and match t")
    for event in events:
        if event.end_s <= event.start_s:
            raise ValueError("event end_s must be greater than start_s")
        mask = _mask(t, event.start_s, event.end_s)
        phases = range(3) if event.phase is None else [event.phase]
        if event.phase is not None and event.phase not in (0, 1, 2):
            raise ValueError("phase must be 0, 1, 2 or None")
        if event.kind not in ("sag", "swell", "interruption"):
            raise ValueError(f"unsupported event kind: {event.kind}")
        for phase in phases:
            if event.kind in ("sag", "swell"):
                x[phase, mask] *= float(event.magnitude)
            else:
                x[phase, mask] = 0.0
    return x


def add_interharmonic(signal, t, frequency_hz, relative_amplitude, phase_rad=0.0, phase_scales=None):
    """Inject a non-integer-frequency component."""
    x = np.asarray(signal, dtype=float).copy()
    if x.ndim != 2 or x.shape[0] != 3 or len(t) != x.shape[1]:
        raise ValueError("signal must have shape [3, samples] and match t")
    rms = np.sqrt(np.mean(x * x, axis=1))
    scales = np.ones(3) if phase_scales is None else np.asarray(phase_scales, dtype=float)
    if scales.shape != (3,):
        raise ValueError("phase_scales must have length 3")
    amp_peak = np.sqrt(2.0) * rms * float(relative_amplitude) * scales
    x += amp_peak[:, None] * np.sin(2*np.pi*frequency_hz*t[None, :] + phase_rad)
    return x


def add_rectifier_ripple(signal, t, ripple_hz=300.0, relative_amplitude=0.02,
                         phase_rad=0.0, phase_scales=None):
    """Model characteristic 6-pulse rectifier/DC-link ripple."""
    return add_interharmonic(signal, t, ripple_hz, relative_amplitude,
                             phase_rad, phase_scales)


def add_switching_transients(signal, t, events, amplitude_v=15.0, decay_s=0.001,
                             ringing_hz=1800.0):
    """Inject short damped ringing bursts representing switching transients."""
    x = np.asarray(signal, dtype=float).copy()
    if x.ndim != 2 or x.shape[0] != 3 or len(t) != x.shape[1]:
        raise ValueError("signal must have shape [3, samples] and match t")
    if decay_s <= 0 or ringing_hz <= 0:
        raise ValueError("decay_s and ringing_hz must be positive")
    for event in events:
        elapsed = np.maximum(t - float(event.start_s), 0.0)
        active = t >= float(event.start_s)
        burst = amplitude_v * np.exp(-elapsed / decay_s) * np.sin(2*np.pi*ringing_hz*elapsed)
        phases = range(3) if event.phase is None else [event.phase]
        for phase in phases:
            x[phase, active] += burst[active]
    return x


def apply_load_step(signal, t, start_s, end_s=None, amplitude_scale=0.9, phase=None):
    """Model a fundamental amplitude step while preserving 50 Hz."""
    x = np.asarray(signal, dtype=float).copy()
    mask = t >= start_s
    if end_s is not None:
        mask &= t < end_s
    phases = range(3) if phase is None else [phase]
    for p in phases:
        x[p, mask] *= float(amplitude_scale)
    return x


def composite_stress(signal, t, fundamental_hz=50.0, seed=7):
    """Deterministic high-stress scenario used for regression benchmarks."""
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
    polluted = add_rectifier_ripple(polluted, t, 300.0, 0.008,
                                    phase_scales=[1.0, 0.9, 1.1])
    polluted = add_switching_transients(
        polluted, t,
        [Event(0.115, 0.115, "switch", 1.0, phase=0),
         Event(0.162, 0.162, "switch", 1.0, phase=None)],
        amplitude_v=12.0, decay_s=0.0008, ringing_hz=2200.0)
    polluted = apply_load_step(polluted, t, 0.045, 0.07, 0.92, phase=1)
    events = [
        Event(0.07, 0.095, "sag", 0.82, phase=None),
        Event(0.13, 0.145, "swell", 1.10, phase=1),
        Event(0.18, 0.185, "interruption", 0.0, phase=2),
    ]
    polluted = apply_voltage_events(polluted, t, events)
    polluted += rng.normal(0.0, 0.05, size=polluted.shape)
    return polluted, events
