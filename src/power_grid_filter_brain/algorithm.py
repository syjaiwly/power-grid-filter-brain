from abc import ABC, abstractmethod
import numpy as np


class AlgorithmBrain(ABC):
    @abstractmethod
    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        raise NotImplementedError


class PassthroughBrain(AlgorithmBrain):
    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        return polluted_signal.copy()


class Fundamental50HzBrain(AlgorithmBrain):
    """v0.6 reference brain.

    Grid frequency is a fixed system specification: 50 Hz.
    Nominal three-phase voltage is 380 V line-to-line (220 V phase RMS).

    The actual fundamental amplitude and phase are estimated online from the
    contaminated waveform and reconstructed over sliding windows.
    """

    def __init__(self, fundamental_hz=50.0, window_cycles=2.0):
        self.fundamental_hz = fundamental_hz
        self.window_cycles = window_cycles
        self.state_history = []

    def _estimate_block(self, x, sample_rate_hz):
        n = x.shape[-1]
        t = np.arange(n) / sample_rate_hz
        phase = 2 * np.pi * self.fundamental_hz * t
        A = np.column_stack([np.sin(phase), np.cos(phase)])
        coeff = x @ np.linalg.pinv(A).T
        sin_c = coeff[:, 0]
        cos_c = coeff[:, 1]
        amplitude_rms = np.hypot(sin_c, cos_c) / np.sqrt(2.0)
        phase_rad = np.arctan2(cos_c, sin_c)
        recon = (
            sin_c[:, None] * np.sin(phase)[None, :]
            + cos_c[:, None] * np.cos(phase)[None, :]
        )
        return amplitude_rms, phase_rad, recon

    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        x = np.asarray(polluted_signal, dtype=float)
        n = x.shape[-1]
        samples_per_cycle = sample_rate_hz / self.fundamental_hz
        win = max(32, int(round(samples_per_cycle * self.window_cycles)))
        hop = max(1, win // 4)

        out = np.zeros_like(x)
        weights = np.zeros(n)
        self.state_history = []

        for start in range(0, n, hop):
            end = min(n, start + win)
            start = max(0, end - win)
            if end - start < 32:
                break

            block = x[:, start:end]
            amp_rms, phase_rad, recon = self._estimate_block(block, sample_rate_hz)
            self.state_history.append({
                "time_s": (start + end) / 2 / sample_rate_hz,
                "amplitude_rms_v": amp_rms.copy(),
                "phase_rad": phase_rad.copy(),
            })

            w = np.hanning(end - start)
            if np.all(w == 0):
                w = np.ones(end - start)
            out[:, start:end] += recon * w[None, :]
            weights[start:end] += w

        weights[weights == 0] = 1.0
        return out / weights[None, :]
