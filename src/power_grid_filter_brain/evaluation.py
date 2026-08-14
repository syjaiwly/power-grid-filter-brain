import numpy as np


def rmse(reference, estimate):
    return float(np.sqrt(np.mean((np.asarray(reference) - np.asarray(estimate)) ** 2)))


def snr_db(reference, estimate):
    ref = np.asarray(reference)
    err = ref - np.asarray(estimate)
    p_signal = np.mean(ref ** 2)
    p_error = max(np.mean(err ** 2), 1e-30)
    return float(10 * np.log10(p_signal / p_error))


def thd_percent(signal, fundamental_hz, sample_rate_hz):
    x = np.asarray(signal)
    if x.ndim > 1:
        x = x[0]
    n = len(x)
    spec = np.fft.rfft(x * np.hanning(n))
    freqs = np.fft.rfftfreq(n, 1 / sample_rate_hz)
    k1 = np.argmin(np.abs(freqs - fundamental_hz))
    fund = abs(spec[k1])
    harm_sq = 0.0
    for k in range(2, 40):
        kh = np.argmin(np.abs(freqs - k * fundamental_hz))
        harm_sq += abs(spec[kh]) ** 2
    return float(100 * np.sqrt(harm_sq) / max(fund, 1e-30))


def evaluate(reference, polluted, filtered, sample_rate_hz, fundamental_hz=50.0):
    return {
        "rmse_input_v": rmse(reference, polluted),
        "rmse_output_v": rmse(reference, filtered),
        "snr_input_db": snr_db(reference, polluted),
        "snr_output_db": snr_db(reference, filtered),
        "thd_input_percent": thd_percent(polluted, fundamental_hz, sample_rate_hz),
        "thd_output_percent": thd_percent(filtered, fundamental_hz, sample_rate_hz),
    }
