import numpy as np
from power_grid_filter_brain.algorithm import Fundamental50HzBrain


def test_fixed_50hz_amplitude_phase_reconstruction():
    fs = 20_000
    t = np.arange(int(0.2 * fs)) / fs
    amp = 200.0
    phase = 0.08
    x = amp * np.sqrt(2) * np.sin(2*np.pi*50*t + phase)
    three = np.vstack([x, x, x])
    brain = Fundamental50HzBrain(window_cycles=2)
    out = brain.process(three, fs)
    state = brain.state_history[-1]
    assert abs(state["amplitude_rms_v"][0] - amp) < 1.0
    assert abs(state["phase_rad"][0] - phase) < 0.02
    assert np.sqrt(np.mean((out - three)**2)) < 0.5
