from power_grid_filter_brain.algorithm import Fundamental50HzBrain
from power_grid_filter_brain.benchmark import run_benchmark, improvement


def test_benchmark_is_structured_and_repeatable_enough_for_ci():
    result = run_benchmark(Fundamental50HzBrain(window_cycles=2), sample_rate_hz=10_000, duration_s=0.2)
    assert result.samples == 2000
    assert result.runtime_ms >= 0
    metrics = improvement(result)
    assert set(metrics) == {"rmse_reduction_percent", "snr_gain_db", "thd_reduction_percent"}
