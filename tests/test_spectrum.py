"""Reproduction checks for the archived published spectra."""

from pathlib import Path

import analyze_spectrum as spectrum
import numpy as np


def test_spectrum_analysis_is_finite_and_reproducible():
    result = spectrum.main()
    assert result["n"] == 408
    assert len(result["rows"]) == 4
    assert len(result["pairs"]) == 6
    assert all(np.isfinite(row["chi2"]) and row["dof"] == 407 for row in result["rows"])
    assert all(row["reduced_chi2"] > 4 for row in result["rows"])
    assert sorted(row["negative_bins"] for row in result["rows"]) == [0, 0, 0, 2]
    assert all(pair["median_abs_independence_z"] < 1 for pair in result["pairs"])
    for path in (spectrum.STATS_FILE, spectrum.AGREEMENT_FILE,
                 spectrum.FIGURE_FILE, spectrum.AGREEMENT_FIGURE):
        assert Path(path).is_file() and Path(path).stat().st_size > 100
