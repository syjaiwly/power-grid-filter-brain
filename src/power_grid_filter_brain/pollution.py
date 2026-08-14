from dataclasses import dataclass, field
import numpy as np


@dataclass
class Harmonic:
    order: int
    relative_amplitude: float
    phase_rad: float | list[float] = 0.0
    phase_scale: float | list[float] = 1.0


@dataclass
class PollutionConfig:
    harmonics: list[Harmonic] = field(default_factory=list)
    noise_rms_v: float = 0.0
    dc_offset_v: float | list[float] = 0.0
    seed: int = 0


def _three_phase(value, default=0.0):
    if np.isscalar(value):
        return np.full(3, float(value if value is not None else default))
    arr = np.asarray(value, dtype=float)
    if arr.shape != (3,):
        raise ValueError("three-phase parameters must be scalar or length 3")
    return arr


def inject_pollution(signal, fundamental_hz, t, cfg: PollutionConfig):
    """Add controlled pollution without assuming identical distortion in all phases."""
    x = np.asarray(signal, dtype=float).copy()
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2 or x.shape[0] not in (1, 3):
        raise ValueError("signal must have shape [phases, samples]")
    phases = x.shape[0]
    rng = np.random.default_rng(cfg.seed)

    base_rms = np.sqrt(np.mean(x * x, axis=1))
    for h in cfg.harmonics:
        phase = _three_phase(h.phase_rad)[:phases]
        scale = _three_phase(h.phase_scale, 1.0)[:phases]
        amp_peak = np.sqrt(2.0) * base_rms * h.relative_amplitude * scale
        component = amp_peak[:, None] * np.sin(
            2 * np.pi * fundamental_hz * h.order * t[None, :] + phase[:, None]
        )
        x += component

    dc = _three_phase(cfg.dc_offset_v)[:phases]
    x += dc[:, None]

    if cfg.noise_rms_v > 0:
        x += rng.normal(0.0, cfg.noise_rms_v, size=x.shape)
    return x
