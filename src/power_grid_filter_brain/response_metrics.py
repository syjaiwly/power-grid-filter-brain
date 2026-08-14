"""Real-time APF response-time metrics.

These metrics make dynamic performance a first-class acceptance criterion.
The APF must suppress pollution quickly without following the 50 Hz fundamental
as if it were pollution.
"""
from __future__ import annotations

import numpy as np


def settling_time(signal: np.ndarray, target: np.ndarray, step_index: int, fs: float, band: float = 0.1) -> float:
    """Return post-step settling time in seconds, using a relative error band."""
    signal = np.asarray(signal, dtype=float)
    target = np.asarray(target, dtype=float)
    if signal.shape != target.shape or not 0 <= step_index < signal.size:
        raise ValueError("signal/target shape or step_index is invalid")
    scale = max(abs(target[-1] - target[step_index - 1]), 1e-12)
    err = np.abs(signal[step_index:] - target[step_index:]) / scale
    outside = np.flatnonzero(err > band)
    if outside.size == 0:
        return 0.0
    last = outside[-1]
    return float((last + 1) / fs)


def response_summary(signal: np.ndarray, target: np.ndarray, step_index: int, fs: float) -> dict[str, float]:
    """Return 10/90 rise time and 10% settling time for a step-like response."""
    y = np.asarray(signal, dtype=float)
    r = np.asarray(target, dtype=float)
    if y.shape != r.shape:
        raise ValueError("signal and target must have the same shape")
    pre = float(r[step_index - 1])
    final = float(r[-1])
    delta = final - pre
    if abs(delta) < 1e-12:
        raise ValueError("target step is too small")
    z = (y[step_index:] - pre) / delta
    def first_cross(level: float) -> int:
        hit = np.flatnonzero(z >= level) if delta > 0 else np.flatnonzero(z <= 1-level)
        return int(hit[0]) if hit.size else len(z) - 1
    i10 = first_cross(0.10)
    i90 = first_cross(0.90)
    return {
        "rise_time_10_90_s": float((i90 - i10) / fs),
        "settling_time_10pct_s": settling_time(y, r, step_index, fs, band=0.10),
        "peak_overshoot_fraction": float(max(0.0, np.max((y[step_index:] - final) / max(abs(delta), 1e-12)))),
    }
