"""APF control brain: convert measured pollution into compensating current references."""
from dataclasses import dataclass
import numpy as np


@dataclass
class APFReference:
    fundamental: np.ndarray
    compensation: np.ndarray
    residual: np.ndarray


def generate_current_reference(measured_current: np.ndarray,
                               fundamental_current: np.ndarray) -> APFReference:
    """Generate the first APF compensation-current reference.

    Convention: positive compensation is current injected by the APF. If
    measured load current = desired fundamental + pollution, the APF injects
    the negative residual so grid current approaches the desired fundamental.
    """
    i = np.asarray(measured_current, dtype=float)
    f = np.asarray(fundamental_current, dtype=float)
    if i.ndim != 2 or f.shape != i.shape or i.shape[0] != 3:
        raise ValueError("measured_current and fundamental_current must both be 3xN")
    residual = i - f
    return APFReference(fundamental=f, compensation=-residual, residual=residual)
