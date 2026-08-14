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
    """Reference sliding-window 50 Hz estimator.

    This estimator is accurate for offline reconstruction, but its centered
    overlap-add windows are not causal. It is therefore a benchmark reference,
    not yet the final real-time deployment path.
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


class CausalFundamental50HzBrain(AlgorithmBrain):
    """Causal 50 Hz state tracker for real-time deployment experiments.

    Uses synchronous I/Q demodulation followed by a first-order exponential
    low-pass. Every output sample depends only on current and previous samples;
    there is no future-looking window. The trade-off is intentional: faster
    tracking means more ripple, while slower tracking means cleaner state.
    """

    def __init__(self, fundamental_hz=50.0, time_constant_cycles=1.0,
                 initial_rms_v=220.0):
        if fundamental_hz <= 0 or time_constant_cycles <= 0:
            raise ValueError("fundamental_hz and time_constant_cycles must be positive")
        self.fundamental_hz = float(fundamental_hz)
        self.time_constant_cycles = float(time_constant_cycles)
        self.initial_rms_v = float(initial_rms_v)
        self.state_history = []

    @staticmethod
    def _wrap_phase(phi):
        return (phi + np.pi) % (2 * np.pi) - np.pi

    def process(self, polluted_signal: np.ndarray, sample_rate_hz: float) -> np.ndarray:
        x = np.asarray(polluted_signal, dtype=float)
        if x.ndim == 1:
            x = x[None, :]
        if x.ndim != 2 or x.shape[-1] < 2:
            raise ValueError("polluted_signal must be 1-D or 2-D with at least 2 samples")
        if sample_rate_hz <= 2 * self.fundamental_hz:
            raise ValueError("sample_rate_hz must be above the Nyquist rate")

        n = x.shape[-1]
        dt = 1.0 / sample_rate_hz
        tau = self.time_constant_cycles / self.fundamental_hz
        alpha = 1.0 - np.exp(-dt / tau)
        t = np.arange(n) * dt
        wt = 2 * np.pi * self.fundamental_hz * t
        s = np.sin(wt)
        c = np.cos(wt)

        # For x = a*sin(wt)+b*cos(wt), LPF(2*x*sin)=a and LPF(2*x*cos)=b.
        a = np.full(x.shape[0], np.sqrt(2.0) * self.initial_rms_v)
        b = np.zeros(x.shape[0])
        output = np.zeros_like(x)
        self.state_history = []

        for k in range(n):
            a += alpha * (2.0 * x[:, k] * s[k] - a)
            b += alpha * (2.0 * x[:, k] * c[k] - b)
            rms = np.hypot(a, b) / np.sqrt(2.0)
            phase = self._wrap_phase(np.arctan2(b, a))
            output[:, k] = a * s[k] + b * c[k]
            self.state_history.append({
                "time_s": t[k],
                "amplitude_rms_v": rms.copy(),
                "phase_rad": phase.copy(),
            })
        return output
