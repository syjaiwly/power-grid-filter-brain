import numpy as np
from power_grid_filter_brain.grid import GridConfig, balanced_three_phase
from power_grid_filter_brain.scenarios import Event, apply_voltage_events, add_interharmonic, composite_stress


def test_phase_local_sag_only_changes_selected_phase():
    cfg = GridConfig(duration_s=0.1, sample_rate_hz=10_000)
    t, x = balanced_three_phase(cfg)
    y = apply_voltage_events(x, t, [Event(0.04, 0.06, "sag", 0.8, phase=1)])
    mask = (t >= 0.04) & (t < 0.06)
    assert np.allclose(y[0, mask], x[0, mask])
    assert np.allclose(y[2, mask], x[2, mask])
    assert np.allclose(y[1, mask], 0.8 * x[1, mask])


def test_interharmonic_changes_signal_deterministically():
    cfg = GridConfig(duration_s=0.1, sample_rate_hz=10_000)
    t, x = balanced_three_phase(cfg)
    y1 = add_interharmonic(x, t, 83.0, 0.01, phase_scales=[1, 0.8, 1.2])
    y2 = add_interharmonic(x, t, 83.0, 0.01, phase_scales=[1, 0.8, 1.2])
    assert not np.allclose(y1, x)
    assert np.allclose(y1, y2)


def test_composite_stress_is_reproducible():
    cfg = GridConfig(duration_s=0.25, sample_rate_hz=10_000)
    t, x = balanced_three_phase(cfg)
    y1, events1 = composite_stress(x, t)
    y2, events2 = composite_stress(x, t)
    assert len(events1) == 3
    assert events1 == events2
    assert np.allclose(y1, y2)
