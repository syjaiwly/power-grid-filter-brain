"""Multi-time-scale detector for APF compensation reference generation.

v2.0 design:
- fast half-cycle detector for early evidence;
- one-cycle detector for confirmation;
- both are causal and use the fixed 50 Hz grid prior only as a reference;
- confirmation prevents a single noisy fast estimate from immediately becoming
  a large compensation command.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class MultiRateDecision:
    fast_amplitude: float
    slow_amplitude: float
    confirmed: bool
    compensation_amplitude: float


class MultiRateHarmonicDetector:
    """Causal fast-discovery/slow-confirmation harmonic detector."""

    def __init__(self, fs: float, frequency: float, threshold: float):
        if fs <= 0 or frequency <= 0:
            raise ValueError("fs and frequency must be positive")
        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        self.fs = float(fs)
        self.frequency = float(frequency)
        self.threshold = float(threshold)
        self._phase = 0.0
        self._fast_n = max(4, int(round(0.5 * fs / frequency)))
        self._slow_n = max(4, int(round(1.0 * fs / frequency)))
        self._buffer = np.zeros(self._slow_n)
        self._count = 0

    def update(self, sample: float) -> MultiRateDecision:
        """Consume one sample and return the current causal decision."""
        self._buffer[:-1] = self._buffer[1:]
        self._buffer[-1] = sample
        self._count = min(self._count + 1, self._slow_n)

        n = self._count
        idx = np.arange(n)
        # The buffer is chronological only after enough samples; use the tail.
        x = self._buffer[-n:]
        phase = self._phase - (n - 1 - idx) * 2.0 * np.pi * self.frequency / self.fs
        s = np.sin(phase)
        c = np.cos(phase)

        def amplitude(window: int) -> float:
            if n < window:
                return 0.0
            z = self._buffer[-window:]
            j = np.arange(window)
            ph = self._phase - (window - 1 - j) * 2.0 * np.pi * self.frequency / self.fs
            si = np.sin(ph)
            co = np.cos(ph)
            I = 2.0 / window * float(np.dot(z, si))
            Q = 2.0 / window * float(np.dot(z, co))
            return float(np.hypot(I, Q))

        fast = amplitude(self._fast_n)
        slow = amplitude(self._slow_n)
        confirmed = fast >= self.threshold and slow >= self.threshold
        compensation = fast if confirmed else 0.0
        self._phase = (self._phase + 2.0 * np.pi * self.frequency / self.fs) % (2.0 * np.pi)
        return MultiRateDecision(fast, slow, confirmed, compensation)


def fuse_fast_and_slow(fast_amplitude: np.ndarray,
                        slow_amplitude: np.ndarray,
                        threshold: float) -> np.ndarray:
    """Vectorized reference-generation rule used by the v2.0 experiments."""
    fast = np.asarray(fast_amplitude, dtype=float)
    slow = np.asarray(slow_amplitude, dtype=float)
    if fast.shape != slow.shape:
        raise ValueError("fast and slow arrays must have the same shape")
    confirmed = (fast >= threshold) & (slow >= threshold)
    return np.where(confirmed, fast, 0.0)
