from dataclasses import dataclass, field
import numpy as np


@dataclass
class Harmonic:
    order: int
    relative_amplitude: float
    phase_rad: float = 0.0


@dataclass
class PollutionConfig:
    harmonics: list[Harmonic] = field(default_factory=list)
    noise_rms_v: float = 0.0
    seed: int = 0


def inject_pollution(signal, fundamental_hz, t, cfg: PollutionConfig):
    x = np.asarray(signal, dtype=float).copy()
    rng = np.random.default_rng(cfg.seed)
    base_peak = np.sqrt(2.0) * np.max(np.sqrt(np.mean(x * x, axis=1)))
    for h in cfg.harmonics:
        amp = base_peak * h.relative_amplitude
        x += amp * np.sin(2*np.pi*fundamental_hz*h.order*t + h.phase_rad)[None, :]
    if cfg.noise_rms_v > 0:
        x += rng.normal(0.0, cfg.noise_rms_v, size=x.shape)
    return x
