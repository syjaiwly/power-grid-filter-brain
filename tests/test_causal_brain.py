import numpy as np
from power_grid_filter_brain.algorithm import CausalFundamental50HzBrain


def test_causal_brain_tracks_50hz_amplitude_without_future_samples():
    fs = 20_000
    t = np.arange(int(0.25 * fs)) / fs
    amp = np.where(t < 0.12, 220.0, 190.0)
    x = np.sqrt(2) * amp[None, :] * np.sin(2*np.pi*50*t)[None, :]
    x = np.repeat(x, 3, axis=0)
    brain = CausalFundamental50HzBrain(time_constant_cycles=0.5)
    y = brain.process(x, fs)
    states = np.array([s["amplitude_rms_v"][0] for s in brain.state_history])
    assert y.shape == x.shape
    assert abs(np.mean(states[int(.08*fs):int(.11*fs)]) - 220) < 8
    assert states[-1] < 205


def test_causal_brain_rejects_invalid_rate():
    brain = CausalFundamental50HzBrain()
    x = np.zeros((3, 100))
    try:
        brain.process(x, 80)
    except ValueError:
        return
    raise AssertionError("expected Nyquist validation error")
