"""Reduced-order nonlinear rectifier load model for APF stress tests.

This is intentionally a simulation model, not a hardware driver. It produces
capacitor-charging current pulses from a three-phase voltage waveform and
provides deterministic metrics for APF response testing.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RectifierLoadConfig:
    dc_cap_voltage: float = 300.0
    diode_drop: float = 1.5
    load_resistance: float = 12.0
    dc_capacitance: float = 2200e-6


def simulate_dc_link_rectifier(
    phase_voltage: np.ndarray,
    fs: float,
    config: RectifierLoadConfig = RectifierLoadConfig(),
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate a three-phase diode bridge feeding a DC capacitor/resistor.

    Parameters
    ----------
    phase_voltage:
        Array shaped (3, N), phase-to-neutral voltage in volts.
    fs:
        Sampling frequency in Hz.
    config:
        Reduced-order bridge/DC-link parameters.

    Returns
    -------
    load_current:
        Three-phase current drawn from the AC source, shaped (3, N).
    dc_voltage:
        DC-link voltage, shaped (N,).

    Notes
    -----
    The model uses the phase with the highest instantaneous positive voltage
    and the lowest negative voltage to represent the conducting diode pair.
    It is suitable for controller development and stress tests; switching
    device reverse recovery and parasitic capacitances are intentionally left
    for the higher-fidelity power-stage model.
    """
    v = np.asarray(phase_voltage, dtype=float)
    if v.ndim != 2 or v.shape[0] != 3:
        raise ValueError("phase_voltage must have shape (3, N)")
    if fs <= 0:
        raise ValueError("fs must be positive")

    n = v.shape[1]
    dt = 1.0 / fs
    i_ac = np.zeros_like(v)
    vdc = np.empty(n, dtype=float)
    vdc[0] = min(config.dc_cap_voltage, np.max(v[:, 0]) - np.min(v[:, 0]))

    for k in range(1, n):
        hi = int(np.argmax(v[:, k]))
        lo = int(np.argmin(v[:, k]))
        bridge_voltage = max(0.0, v[hi, k] - v[lo, k] - 2.0 * config.diode_drop)
        dc_load = max(vdc[k - 1], 0.0) / max(config.load_resistance, 1e-9)

        # Charging is enabled only when the bridge can exceed the capacitor.
        if bridge_voltage > vdc[k - 1]:
            # Small source resistance surrogate keeps the numerical model bounded.
            charge_current = (bridge_voltage - vdc[k - 1]) / 0.35
            i_ac[hi, k] += charge_current
            i_ac[lo, k] -= charge_current
        else:
            charge_current = 0.0

        dv = (charge_current - dc_load) / max(config.dc_capacitance, 1e-12)
        vdc[k] = max(0.0, vdc[k - 1] + dt * dv)

    return i_ac, vdc


def harmonic_rms(signal: np.ndarray, fundamental_rms: float) -> float:
    """Return RMS of the non-fundamental residual for a reference waveform."""
    x = np.asarray(signal, dtype=float)
    ref = np.sqrt(2.0) * fundamental_rms
    return float(np.sqrt(max(np.mean(x * x) - 0.5 * ref * ref, 0.0)))
