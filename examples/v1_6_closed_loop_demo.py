import numpy as np
from power_grid_filter_brain.apf_control import harmonic_compensation_reference
from power_grid_filter_brain.apf_power_stage import ThreePhaseAPFPowerStage

fs = 20_000.0
t = np.arange(int(0.12 * fs)) / fs
f = 50.0
fundamental = np.vstack([
    np.sqrt(2)*10*np.sin(2*np.pi*f*t),
    np.sqrt(2)*10*np.sin(2*np.pi*f*t - 2*np.pi/3),
    np.sqrt(2)*10*np.sin(2*np.pi*f*t + 2*np.pi/3),
])
pollution = np.vstack([
    2*np.sin(2*np.pi*250*t) + np.sin(2*np.pi*350*t),
    1.6*np.sin(2*np.pi*250*t) + .8*np.sin(2*np.pi*450*t),
    1.8*np.sin(2*np.pi*350*t) + .7*np.sin(2*np.pi*550*t),
])
load = fundamental + pollution
reference = harmonic_compensation_reference(load, fundamental, max_current_a=30)
stage = ThreePhaseAPFPowerStage(fs, 1500, 30)
compensation, grid = stage.run(reference, load)

before = np.sqrt(np.mean(pollution**2, axis=1))
after = np.sqrt(np.mean((grid - fundamental)**2, axis=1))
print("pollution RMS A:", np.round(before, 4))
print("post-APF residual RMS A:", np.round(after, 4))
print("average pollution reduction %:", round((1 - after.mean()/before.mean()) * 100, 2))
