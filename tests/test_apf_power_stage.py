import numpy as np
from power_grid_filter_brain.apf_control import harmonic_compensation_reference
from power_grid_filter_brain.apf_power_stage import ThreePhaseAPFPowerStage


def test_apf_stage_reduces_harmonic_residual():
    fs = 20_000
    t = np.arange(int(0.12 * fs)) / fs
    f = 50.0
    fundamental = np.vstack([
        np.sqrt(2)*10*np.sin(2*np.pi*f*t),
        np.sqrt(2)*10*np.sin(2*np.pi*f*t-2*np.pi/3),
        np.sqrt(2)*10*np.sin(2*np.pi*f*t+2*np.pi/3),
    ])
    pollution = np.vstack([
        2*np.sin(2*np.pi*250*t)+1*np.sin(2*np.pi*350*t),
        1.6*np.sin(2*np.pi*250*t)+.8*np.sin(2*np.pi*450*t),
        1.8*np.sin(2*np.pi*350*t)+.7*np.sin(2*np.pi*550*t),
    ])
    load = fundamental + pollution
    ref = harmonic_compensation_reference(load, fundamental, max_current_a=30)
    stage = ThreePhaseAPFPowerStage(fs, 1500, 30)
    _, grid = stage.run(ref, load)
    before = np.sqrt(np.mean((load-fundamental)**2))
    after = np.sqrt(np.mean((grid-fundamental)**2))
    assert after < before
