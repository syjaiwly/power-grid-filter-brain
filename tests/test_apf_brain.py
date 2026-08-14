import numpy as np
from power_grid_filter_brain.apf_brain import generate_current_reference


def test_apf_compensation_cancels_pollution():
    t = np.arange(4000) / 20000.0
    fundamental = np.vstack([
        np.sqrt(2)*10*np.sin(2*np.pi*50*t),
        np.sqrt(2)*10*np.sin(2*np.pi*50*t-2*np.pi/3),
        np.sqrt(2)*10*np.sin(2*np.pi*50*t+2*np.pi/3),
    ])
    pollution = np.vstack([
        2*np.sin(2*np.pi*250*t),
        1.5*np.sin(2*np.pi*350*t),
        1.0*np.sin(2*np.pi*550*t),
    ])
    measured = fundamental + pollution
    ref = generate_current_reference(measured, fundamental)
    grid_after_comp = measured + ref.compensation
    assert np.max(np.abs(ref.compensation + pollution)) < 1e-10
    assert np.sqrt(np.mean((grid_after_comp-fundamental)**2)) < 1e-10
