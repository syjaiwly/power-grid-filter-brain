import numpy as np
from dataclasses import dataclass


@dataclass
class GridConfig:
    frequency_hz: float = 50.0
    line_voltage_rms_v: float = 380.0
    phase_voltage_rms_v: float = 220.0
    sample_rate_hz: float = 10_000.0
    duration_s: float = 0.2


def time_axis(cfg: GridConfig):
    n = int(round(cfg.sample_rate_hz * cfg.duration_s))
    return np.arange(n) / cfg.sample_rate_hz


def balanced_three_phase(cfg: GridConfig):
    t = time_axis(cfg)
    peak = cfg.phase_voltage_rms_v * np.sqrt(2.0)
    w = 2 * np.pi * cfg.frequency_hz
    x = np.vstack([
        peak * np.sin(w * t),
        peak * np.sin(w * t - 2 * np.pi / 3),
        peak * np.sin(w * t + 2 * np.pi / 3),
    ])
    return t, x
