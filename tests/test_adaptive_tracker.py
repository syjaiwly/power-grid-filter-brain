import numpy as np
from power_grid_filter_brain.algorithm import AdaptiveCausalFundamental50HzBrain


def test_adaptive_tracker_preserves_fundamental_step_and_rejects_5th_harmonic():
    fs=20_000; t=np.arange(int(.24*fs))/fs
    amp=np.where(t<.10,220.0,255.0)
    fundamental=np.sqrt(2)*amp*np.sin(2*np.pi*50*t)
    polluted=fundamental+0.12*np.sqrt(2)*220*np.sin(2*np.pi*250*t)
    brain=AdaptiveCausalFundamental50HzBrain()
    out=brain.process(polluted,fs)[0]
    post=t>=.18
    assert abs(np.sqrt(np.mean(out[post]**2))-255.0)<8.0
    harmonic_only=np.sin(2*np.pi*250*t)
    hbrain=AdaptiveCausalFundamental50HzBrain()
    hout=hbrain.process(harmonic_only,fs)[0]
    assert np.sqrt(np.mean(hout[int(.18*fs):]**2))<0.20
