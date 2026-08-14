from abc import ABC, abstractmethod
import numpy as np


class AlgorithmBrain(ABC):
    @abstractmethod
    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        raise NotImplementedError


class PassthroughBrain(AlgorithmBrain):
    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        return np.asarray(polluted_signal, dtype=float).copy()


class Fundamental50HzBrain(AlgorithmBrain):
    """Real-time 50 Hz fundamental state estimator.

    50 Hz is a fixed grid prior. Fundamental RMS amplitude and phase are
    estimated independently for every input phase. The phase estimate is
    referenced to absolute time, so state history is directly comparable
    across sliding windows.
    """

    def __init__(self, fundamental_hz=50.0, window_cycles=2.0):
        if fundamental_hz <= 0 or window_cycles <= 0:
            raise ValueError("fundamental_hz and window_cycles must be positive")
        self.fundamental_hz = float(fundamental_hz)
        self.window_cycles = float(window_cycles)
        self.state_history = []

    @staticmethod
    def _wrap_phase(phi):
        return (phi + np.pi) % (2 * np.pi) - np.pi

    def _estimate_block(self, x, sample_rate_hz, start_time_s):
        n = x.shape[-1]
        t = start_time_s + np.arange(n) / sample_rate_hz
        wt = 2 * np.pi * self.fundamental_hz * t
        design = np.column_stack((np.sin(wt), np.cos(wt)))
        coeff = x @ np.linalg.pinv(design).T
        sin_coeff, cos_coeff = coeff[:, 0], coeff[:, 1]
        amplitude_rms = np.hypot(sin_coeff, cos_coeff) / np.sqrt(2.0)
        phase_rad = self._wrap_phase(np.arctan2(cos_coeff, sin_coeff))
        reconstruction = (
            sin_coeff[:, None] * np.sin(wt)[None, :]
            + cos_coeff[:, None] * np.cos(wt)[None, :]
        )
        return amplitude_rms, phase_rad, reconstruction

    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        x = np.asarray(polluted_signal, dtype=float)
        if x.ndim == 1:
            x = x[None, :]
        if x.ndim != 2 or x.shape[-1] < 32:
            raise ValueError("polluted_signal must be 1-D or 2-D with at least 32 samples")
        if sample_rate_hz <= 2 * self.fundamental_hz:
            raise ValueError("sample_rate_hz must be above the Nyquist rate")

        n = x.shape[-1]
        samples_per_cycle = sample_rate_hz / self.fundamental_hz
        window = max(32, int(round(samples_per_cycle * self.window_cycles)))
        hop = max(1, window // 4)

        output = np.zeros_like(x)
        weights = np.zeros(n)
        self.state_history = []

        for start in range(0, n, hop):
            end = min(n, start + window)
            start = max(0, end - window)
            if end - start < 32:
                break

            amp_rms, phase_rad, reconstruction = self._estimate_block(
                x[:, start:end], sample_rate_hz, start / sample_rate_hz
            )
            self.state_history.append({
                "time_s": (start + end) / (2 * sample_rate_hz),
                "amplitude_rms_v": amp_rms.copy(),
                "phase_rad": phase_rad.copy(),
            })

            weight = np.hanning(end - start)
            if not np.any(weight):
                weight = np.ones(end - start)
            output[:, start:end] += reconstruction * weight[None, :]
            weights[start:end] += weight

        weights[weights == 0] = 1.0
        return output / weights[None, :]
