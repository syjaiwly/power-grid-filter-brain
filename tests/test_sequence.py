import numpy as np
from power_grid_filter_brain.sequence import sequence_magnitudes


def test_balanced_three_phase_is_positive_sequence():
    mag = sequence_magnitudes(
        [220, 220, 220],
        [0, -2*np.pi/3, 2*np.pi/3],
    )
    assert mag["positive"] > 219
    assert mag["negative"] < 1e-8
    assert mag["zero"] < 1e-8


def test_unbalance_creates_negative_sequence():
    mag = sequence_magnitudes(
        [220, 200, 220],
        [0, -2*np.pi/3, 2*np.pi/3],
    )
    assert mag["negative"] > 5
