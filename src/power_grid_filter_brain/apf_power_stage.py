import numpy as np


class ThreePhaseAPFPowerStage:
    """Reduced-order APF power-stage model for controller development.

    This is a control-development model, not a switching-device SPICE model.
    It represents the APF as a three-phase current source behind a first-order
    current-loop plant. The model makes sensor/actuator dynamics explicit so
    the reference generator can be evaluated before adding PWM/device detail.
    """

    def __init__(self, sample_rate_hz=20_000.0, current_loop_bandwidth_hz=1_500.0,
                 max_compensation_current_a=30.0):
        if sample_rate_hz <= 0 or current_loop_bandwidth_hz <= 0:
            raise ValueError("sample_rate_hz and current_loop_bandwidth_hz must be positive")
        if max_compensation_current_a <= 0:
            raise ValueError("max_compensation_current_a must be positive")
        self.sample_rate_hz = float(sample_rate_hz)
        self.current_loop_bandwidth_hz = float(current_loop_bandwidth_hz)
        self.max_compensation_current_a = float(max_compensation_current_a)
        self._state = np.zeros(3)

    def reset(self):
        self._state[:] = 0.0

    def step(self, reference_compensation_a, measured_load_a):
        ref = np.asarray(reference_compensation_a, dtype=float)
        load = np.asarray(measured_load_a, dtype=float)
        if ref.shape != load.shape or ref.ndim != 1 or ref.size != 3:
            raise ValueError("reference_compensation_a and measured_load_a must each be shape (3,)")
        dt = 1.0 / self.sample_rate_hz
        alpha = 1.0 - np.exp(-2.0 * np.pi * self.current_loop_bandwidth_hz * dt)
        limited = np.clip(ref, -self.max_compensation_current_a, self.max_compensation_current_a)
        self._state += alpha * (limited - self._state)
        return self._state.copy(), load + self._state

    def run(self, reference_compensation, measured_load):
        ref = np.asarray(reference_compensation, dtype=float)
        load = np.asarray(measured_load, dtype=float)
        if ref.shape != load.shape or ref.ndim != 2 or ref.shape[0] != 3:
            raise ValueError("inputs must have shape (3, N)")
        self.reset()
        compensation = np.zeros_like(ref)
        grid = np.zeros_like(load)
        for k in range(ref.shape[1]):
            compensation[:, k], grid[:, k] = self.step(ref[:, k], load[:, k])
        return compensation, grid
