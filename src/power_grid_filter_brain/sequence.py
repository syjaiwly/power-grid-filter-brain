import numpy as np


def phase_phasors(amplitude_rms_v, phase_rad):
    """Build RMS complex phase phasors [A, B, C]."""
    amp = np.asarray(amplitude_rms_v, dtype=float)
    phase = np.asarray(phase_rad, dtype=float)
    if amp.shape != (3,) or phase.shape != (3,):
        raise ValueError("expected three phase amplitudes and phases")
    return amp * np.exp(1j * phase)


def symmetrical_components(phasors):
    """Return zero, positive and negative sequence RMS phasors."""
    v = np.asarray(phasors, dtype=complex)
    if v.shape != (3,):
        raise ValueError("phasors must contain [A, B, C]")
    a = np.exp(1j * 2 * np.pi / 3)
    zero = (v[0] + v[1] + v[2]) / 3
    positive = (v[0] + a * v[1] + a**2 * v[2]) / 3
    negative = (v[0] + a**2 * v[1] + a * v[2]) / 3
    return {"zero": zero, "positive": positive, "negative": negative}


def sequence_magnitudes(amplitude_rms_v, phase_rad):
    seq = symmetrical_components(phase_phasors(amplitude_rms_v, phase_rad))
    return {name: float(abs(value)) for name, value in seq.items()}
