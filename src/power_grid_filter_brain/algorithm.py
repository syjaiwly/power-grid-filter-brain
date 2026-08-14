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
    """Offline reference estimator using a sliding 50 Hz window."""
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
        a, b = coeff[:, 0], coeff[:, 1]
        rms = np.hypot(a, b) / np.sqrt(2.0)
        phase = self._wrap_phase(np.arctan2(b, a))
        reconstruction = a[:, None] * np.sin(wt)[None, :] + b[:, None] * np.cos(wt)[None, :]
        return rms, phase, reconstruction

    def process(self, polluted_signal, sample_rate_hz):
        x = np.asarray(polluted_signal, dtype=float)
        if x.ndim == 1: x = x[None, :]
        if x.ndim != 2 or x.shape[-1] < 32: raise ValueError("signal must be 1-D or 2-D with at least 32 samples")
        if sample_rate_hz <= 2 * self.fundamental_hz: raise ValueError("sample_rate_hz must be above Nyquist")
        n = x.shape[-1]; win = max(32, int(round(sample_rate_hz / self.fundamental_hz * self.window_cycles))); hop = max(1, win // 4)
        output = np.zeros_like(x); weights = np.zeros(n); self.state_history = []
        for start in range(0, n, hop):
            end = min(n, start + win); start = max(0, end - win)
            if end - start < 32: break
            rms, phase, reconstruction = self._estimate_block(x[:, start:end], sample_rate_hz, start / sample_rate_hz)
            self.state_history.append({"time_s": (start + end)/(2*sample_rate_hz), "amplitude_rms_v": rms.copy(), "phase_rad": phase.copy()})
            w = np.hanning(end-start); w = w if np.any(w) else np.ones(end-start)
            output[:, start:end] += reconstruction*w[None, :]; weights[start:end] += w
        weights[weights == 0] = 1.0
        return output / weights[None, :]


class CausalFundamental50HzBrain(AlgorithmBrain):
    """Strictly causal real-time 50 Hz I/Q state tracker."""
    def __init__(self, fundamental_hz=50.0, time_constant_cycles=1.0, initial_rms_v=220.0):
        if fundamental_hz <= 0 or time_constant_cycles <= 0:
            raise ValueError("fundamental_hz and time_constant_cycles must be positive")
        self.fundamental_hz = float(fundamental_hz)
        self.time_constant_cycles = float(time_constant_cycles)
        self.initial_rms_v = float(initial_rms_v)
        self.state_history = []

    @staticmethod
    def _wrap_phase(phi):
        return (phi + np.pi) % (2 * np.pi) - np.pi

    def process(self, polluted_signal, sample_rate_hz):
        x = np.asarray(polluted_signal, dtype=float)
        if x.ndim == 1: x = x[None, :]
        if x.ndim != 2 or x.shape[-1] < 2: raise ValueError("signal must be 1-D or 2-D with at least 2 samples")
        if sample_rate_hz <= 2 * self.fundamental_hz: raise ValueError("sample_rate_hz must be above Nyquist")
        n = x.shape[-1]; dt = 1.0/sample_rate_hz
        tau = self.time_constant_cycles/self.fundamental_hz
        alpha = 1.0 - np.exp(-dt/tau)
        t = np.arange(n)*dt; wt = 2*np.pi*self.fundamental_hz*t; s=np.sin(wt); c=np.cos(wt)
        a=np.full(x.shape[0], np.sqrt(2)*self.initial_rms_v); b=np.zeros(x.shape[0])
        output=np.zeros_like(x); self.state_history=[]
        for k in range(n):
            a += alpha*(2*x[:,k]*s[k]-a); b += alpha*(2*x[:,k]*c[k]-b)
            output[:,k] = a*s[k] + b*c[k]
            self.state_history.append({"time_s":t[k], "amplitude_rms_v":np.hypot(a,b)/np.sqrt(2), "phase_rad":self._wrap_phase(np.arctan2(b,a))})
        return output

    def latency_seconds(self):
        return self.time_constant_cycles / self.fundamental_hz


class FundamentalChangeDetector:
    """Causal detector for changes in the 50 Hz fundamental state.

    Current and previous non-overlapping windows are compared. A complete new
    cycle is therefore available before a state-change decision is made.
    """
    def __init__(self, fundamental_hz=50.0, window_cycles=1.0, threshold=0.20):
        if fundamental_hz <= 0 or window_cycles <= 0 or not 0 < threshold < 1:
            raise ValueError("invalid detector parameters")
        self.fundamental_hz = float(fundamental_hz)
        self.window_cycles = float(window_cycles)
        self.threshold = float(threshold)

    @staticmethod
    def _phasor(z, ss, cc):
        z = z - np.mean(z, axis=1, keepdims=True)
        scale = 1.0 / max(z.shape[-1] / 2.0, 1.0)
        return np.sum(z*ss[None, :], axis=1)*scale + 1j*np.sum(z*cc[None, :], axis=1)*scale, z

    def detect(self, signal, sample_rate_hz):
        x = np.asarray(signal, dtype=float)
        if x.ndim == 1: x = x[None, :]
        if x.ndim != 2: raise ValueError("signal must be 1-D or 2-D")
        n = x.shape[-1]
        win = max(16, int(round(sample_rate_hz / self.fundamental_hz * self.window_cycles)))
        t = np.arange(n) / sample_rate_hz
        s = np.sin(2*np.pi*self.fundamental_hz*t); c = np.cos(2*np.pi*self.fundamental_hz*t)
        confidence = np.zeros(n); coherence = np.zeros(n)
        first = 2*win-1
        for k in range(first, n):
            cur = x[:, k-win+1:k+1]
            prev = x[:, k-2*win+1:k-win+1]
            current, cur_centered = self._phasor(cur, s[k-win+1:k+1], c[k-win+1:k+1])
            previous, _ = self._phasor(prev, s[k-2*win+1:k-win+1], c[k-2*win+1:k-win+1])
            proj_energy = np.sum(np.abs(current)**2)
            total_energy = np.sum(cur_centered*cur_centered) * (2.0/max(win/2.0,1.0))
            coh = np.sqrt(np.clip(proj_energy / max(total_energy, 1e-30), 0.0, 1.0))
            coherence[k] = coh
            delta = np.sqrt(np.sum(np.abs(current-previous)**2)) / max(np.sqrt(np.sum(np.abs(previous)**2)), 1e-9)
            confidence[k] = float(np.clip(coh*delta, 0.0, 1.0))
        return {"confidence": confidence, "coherence": coherence, "is_fundamental_change": confidence >= self.threshold}
