import numpy as np
from power_grid_filter_brain.grid import GridConfig, balanced_three_phase
from power_grid_filter_brain.scenarios import (
    Event, apply_voltage_events, add_interharmonic, add_rectifier_ripple,
    add_switching_transients, apply_load_step, composite_stress,
)


def base():
    cfg = GridConfig(duration_s=0.25, sample_rate_hz=20_000)
    return (*balanced_three_phase(cfg),)


def test_phase_local_sag_only_changes_selected_phase():
    t, x = base()
    y = apply_voltage_events(x, t, [Event(0.05, 0.06, "sag", 0.5, phase=1)])
    mask = (t >= 0.05) & (t < 0.06)
    assert np.allclose(y[0, mask], x[0, mask])
    assert np.allclose(y[2, mask], x[2, mask])
    assert np.allclose(y[1, mask], 0.5 * x[1, mask])


def test_realistic_disturbances_change_signal():
    t, x = base()
    y = add_interharmonic(x, t, 83, 0.02)
    y = add_rectifier_ripple(y, t, 300, 0.01)
    y = add_switching_transients(y, t, [Event(0.1, 0.1, "switch", 1)], amplitude_v=10)
    y = apply_load_step(y, t, 0.15, 0.17, 0.9)
    assert np.sqrt(np.mean((y - x) ** 2)) > 1.0


def test_composite_stress_is_reproducible():
    t, x = base()
    y1, events1 = composite_stress(x, t)
    y2, events2 = composite_stress(x, t)
    assert len(events1) == 3
    assert events1 == events2
    assert np.allclose(y1, y2)
