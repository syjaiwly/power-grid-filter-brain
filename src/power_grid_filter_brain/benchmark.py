"""Repeatable benchmark harness for comparing filter brains."""
from dataclasses import dataclass, asdict
from time import perf_counter
import numpy as np

from .evaluation import evaluate
from .grid import GridConfig, balanced_three_phase
from .scenarios import composite_stress


@dataclass
class BenchmarkResult:
    name: str
    rmse_input_v: float
    rmse_output_v: float
    snr_input_db: float
    snr_output_db: float
    thd_input_percent: float
    thd_output_percent: float
    runtime_ms: float
    samples: int

    def to_dict(self):
        return asdict(self)


def run_benchmark(brain, name="composite-stress", sample_rate_hz=20_000,
                  duration_s=0.25):
    """Run one deterministic benchmark and return comparable metrics."""
    cfg = GridConfig(sample_rate_hz=sample_rate_hz, duration_s=duration_s)
    t, truth = balanced_three_phase(cfg)
    polluted, _ = composite_stress(truth, t, cfg.frequency_hz)

    start = perf_counter()
    filtered = brain.process(polluted, sample_rate_hz)
    runtime_ms = (perf_counter() - start) * 1000.0

    metrics = evaluate(truth, polluted, filtered, sample_rate_hz, cfg.frequency_hz)
    return BenchmarkResult(
        name=name,
        rmse_input_v=metrics["rmse_input_v"],
        rmse_output_v=metrics["rmse_output_v"],
        snr_input_db=metrics["snr_input_db"],
        snr_output_db=metrics["snr_output_db"],
        thd_input_percent=metrics["thd_input_percent"],
        thd_output_percent=metrics["thd_output_percent"],
        runtime_ms=runtime_ms,
        samples=polluted.shape[-1],
    )


def improvement(result: BenchmarkResult):
    """Return normalized improvements; positive is better for every field."""
    return {
        "rmse_reduction_percent": 100.0 * (1 - result.rmse_output_v / max(result.rmse_input_v, 1e-12)),
        "snr_gain_db": result.snr_output_db - result.snr_input_db,
        "thd_reduction_percent": 100.0 * (1 - result.thd_output_percent / max(result.thd_input_percent, 1e-12)),
    }
