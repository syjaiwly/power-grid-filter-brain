import numpy as np
from power_grid_filter_brain.algorithm import Fundamental50HzBrain, FundamentalChangeDetector


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


def test_detector_is_quiet_on_steady_fundamental():
    fs = 20_000
    t = np.arange(int(0.15 * fs)) / fs
    x = np.sin(2*np.pi*50*t)
    result = FundamentalChangeDetector(window_cycles=1).detect(x, fs)
    assert np.max(result["confidence"][int(.06*fs):]) < 0.20


def test_detector_scores_real_fundamental_step_over_5th_harmonic():
    fs = 20_000
    t = np.arange(int(0.20 * fs)) / fs
    amp = np.where(t < .10, 1.0, 1.35)
    step = amp*np.sin(2*np.pi*50*t)
    harmonic = np.sin(2*np.pi*250*t)
    detector = FundamentalChangeDetector(window_cycles=1)
    cs = detector.detect(step, fs)["confidence"]
    ch = detector.detect(harmonic, fs)["confidence"]
    assert np.max(cs[int(.10*fs):int(.13*fs)]) > np.max(ch) + 0.10
