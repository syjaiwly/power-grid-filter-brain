"""Reduced-order APF power-stage model for controller development.

This is intentionally not a semiconductor-level model. It captures the first
physical constraints needed by the APF brain: DC-link headroom, interface
inductance, PWM-equivalent voltage saturation, current dynamics and losses.
"""

import numpy as np


class ThreePhaseAPFPowerStage:
    """Discrete averaged three-phase voltage-source APF stage.

    Per phase: L di/dt = v_inv - v_grid - R i.
    The commanded inverter voltage is limited by an available DC-link voltage
    using a conservative linear modulation limit.
    """

    def __init__(self, sample_rate_hz=20_000.0, dc_link_v=700.0,
                 inductance_h=2e-3, resistance_ohm=0.08,
                 modulation_limit=0.90, current_limit_a=30.0):
        if sample_rate_hz <= 0 or dc_link_v <= 0 or inductance_h <= 0:
            raise ValueError("sample_rate_hz, dc_link_v and inductance_h must be positive")
        if resistance_ohm < 0 or not 0 < modulation_limit <= 1 or current_limit_a <= 0:
            raise ValueError("invalid power-stage limits")
        self.fs = float(sample_rate_hz)
        self.dc_link_v = float(dc_link_v)
        self.L = float(inductance_h)
        self.R = float(resistance_ohm)
        self.modulation_limit = float(modulation_limit)
        self.current_limit_a = float(current_limit_a)
        self.current_a = np.zeros(3)

    @property
    def phase_voltage_limit(self):
        return self.modulation_limit * self.dc_link_v / 2.0

    def reset(self):
        self.current_a[:] = 0.0

    def step(self, voltage_command_v, grid_voltage_v):
        """Advance one sample and return actual APF current."""
        v_cmd = np.asarray(voltage_command_v, dtype=float)
        v_grid = np.asarray(grid_voltage_v, dtype=float)
        if v_cmd.shape != (3,) or v_grid.shape != (3,):
            raise ValueError("voltage_command_v and grid_voltage_v must have shape (3,)")
        v_inv = np.clip(v_cmd, -self.phase_voltage_limit, self.phase_voltage_limit)
        di = (v_inv - v_grid - self.R * self.current_a) / self.L
        self.current_a += di / self.fs
        self.current_a = np.clip(self.current_a, -self.current_limit_a, self.current_limit_a)
        return self.current_a.copy()

    def required_voltage(self, current_reference_a, grid_voltage_v):
        """One-step feed-forward voltage needed to move toward a current reference."""
        i_ref = np.asarray(current_reference_a, dtype=float)
        v_grid = np.asarray(grid_voltage_v, dtype=float)
        if i_ref.shape != (3,) or v_grid.shape != (3,):
            raise ValueError("current_reference_a and grid_voltage_v must have shape (3,)")
        di = (np.clip(i_ref, -self.current_limit_a, self.current_limit_a) - self.current_a) * self.fs
        return v_grid + self.R * self.current_a + self.L * di
