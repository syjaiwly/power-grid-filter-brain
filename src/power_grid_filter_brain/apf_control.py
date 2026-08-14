import numpy as np


def harmonic_compensation_reference(measured_load_a, fundamental_a, max_current_a=None):
    """Generate APF compensation-current reference from measured load current.

    The reference is the negative non-fundamental residual. A real deployment
    must additionally account for reactive-power objectives, unbalance,
    converter limits, DC-link regulation and current-loop dynamics.
    """
    measured = np.asarray(measured_load_a, dtype=float)
    fundamental = np.asarray(fundamental_a, dtype=float)
    if measured.shape != fundamental.shape or measured.ndim != 2 or measured.shape[0] != 3:
        raise ValueError("inputs must have shape (3, N)")
    reference = -(measured - fundamental)
    if max_current_a is not None:
        if max_current_a <= 0:
            raise ValueError("max_current_a must be positive")
        reference = np.clip(reference, -max_current_a, max_current_a)
    return reference
