"""Diagnostics for four reductions of one JWST/NIRISS eclipse.

The reductions share the same photons and are correlated. Flat-spectrum tests
quantify structure within each delivered spectrum; they are not molecular
detections. Pairwise normalized differences use a conservative independence
reference and must not be read as formal consistency p-values.
"""

from __future__ import annotations

import csv
from itertools import combinations, pairwise
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "spectra"
FIGURES = ROOT / "figures"
STATS_FILE = FIGURES / "spectrum_statistics.csv"
AGREEMENT_FILE = FIGURES / "pipeline_agreement.csv"
FIGURE_FILE = FIGURES / "wasp18b_published_spectrum.png"
AGREEMENT_FIGURE = FIGURES / "wasp18b_pipeline_differences.png"


def flat_test(values, errors):
    values, errors = np.asarray(values, float), np.asarray(errors, float)
    good = np.isfinite(values) & np.isfinite(errors) & (errors > 0)
    values, errors = values[good], errors[good]
    weights = 1 / errors**2
    mean = float(np.sum(weights * values) / np.sum(weights))
    statistic = float(np.sum(((values - mean) / errors) ** 2))
    dof = len(values) - 1
    return {
        "n": len(values), "mean_ppm": mean, "chi2": statistic, "dof": dof,
        "reduced_chi2": statistic / dof, "p": float(chi2.sf(statistic, dof)),
        "negative_bins": int(np.sum(values < 0)),
        "negative_fraction": float(np.mean(values < 0)),
        "median_error_ppm": float(np.median(errors)),
    }


def load_reductions():
    reductions = []
    labels = {"nameless": "NAMELESS", "nirhiss": "nirHiss",
              "supreme_spoon": "supreme-SPOON",
              "transitspectroscopy": "transitspectroscopy"}
    for path in sorted(DATA.glob("*_w18b_spectrum.txt")):
        values = np.loadtxt(path)
        key = path.stem.replace("_w18b_spectrum", "")
        reductions.append((labels[key], values[:, 0], values[:, 1], values[:, 2]))
    return reductions


def compare_pair(first, second):
    label_a, wave_a, depth_a, error_a = first
    label_b, wave_b, depth_b, error_b = second
    low, high = max(wave_a.min(), wave_b.min()), min(wave_a.max(), wave_b.max())
    keep = (wave_a >= low) & (wave_a <= high)
    wavelength = wave_a[keep]
    comparison_depth = np.interp(wavelength, wave_b, depth_b)
    comparison_error = np.interp(wavelength, wave_b, error_b)
    difference = depth_a[keep] - comparison_depth
    reference_sigma = np.sqrt(error_a[keep] ** 2 + comparison_error**2)
    normalized = difference / reference_sigma
    return {
        "pair": f"{label_a} - {label_b}", "n_overlap": len(difference),
        "wavelength_min_micron": float(low), "wavelength_max_micron": float(high),
        "median_difference_ppm": float(np.median(difference)),
        "median_absolute_difference_ppm": float(np.median(np.abs(difference))),
        "rms_difference_ppm": float(np.sqrt(np.mean(difference**2))),
        "median_abs_independence_z": float(np.median(np.abs(normalized))),
        "fraction_abs_independence_z_gt_2": float(np.mean(np.abs(normalized) > 2)),
        "wavelength": wavelength, "difference": difference,
        "reference_sigma": reference_sigma,
    }


def write_rows(path, rows):
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def binned(wavelength, values, errors, width=0.04):
    edges = np.arange(wavelength.min(), wavelength.max() + width, width)
    x, y, e = [], [], []
    for left, right in pairwise(edges):
        use = (wavelength >= left) & (wavelength < right)
        if not use.any():
            continue
        weights = 1 / errors[use] ** 2
        x.append(np.sum(weights * wavelength[use]) / np.sum(weights))
        y.append(np.sum(weights * values[use]) / np.sum(weights))
        e.append(np.sqrt(1 / np.sum(weights)))
    return np.asarray(x), np.asarray(y), np.asarray(e)


def main():
    FIGURES.mkdir(exist_ok=True)
    reductions, rows = load_reductions(), []
    fig, ax = plt.subplots(figsize=(9.4, 5.5))
    for label, wavelength, depth, error in reductions:
        result = flat_test(depth, error)
        below_one = wavelength < 1
        rows.append({"comparison": label + " vs weighted flat",
                     "wavelength_min_micron": float(wavelength.min()),
                     "wavelength_max_micron": float(wavelength.max()),
                     "negative_bins_below_1_micron": int(np.sum(depth[below_one] < 0)),
                     "bins_below_1_micron": int(np.sum(below_one)), **result})
        x, y, e = binned(wavelength, depth, error)
        ax.errorbar(x, y, yerr=e, fmt="o-", ms=3, lw=1, alpha=.72, label=label)
    write_rows(STATS_FILE, rows)
    ax.axhline(0, color="#52606d", lw=1, ls="--")
    ax.set(xlabel="Wavelength [µm]", ylabel="Planet/star flux ratio [ppm]",
           title="WASP-18 b — four reductions of one NIRISS/SOSS eclipse")
    ax.grid(alpha=.2)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURE_FILE, dpi=200)
    plt.close(fig)

    pairs = [compare_pair(a, b) for a, b in combinations(reductions, 2)]
    write_rows(AGREEMENT_FILE, [{key: value for key, value in pair.items()
                                 if key not in {"wavelength", "difference", "reference_sigma"}}
                                for pair in pairs])
    fig, axes = plt.subplots(len(pairs), 1, figsize=(9.5, 12.2), sharex=True)
    for ax, pair in zip(axes, pairs):
        ax.axhline(0, color="#52606d", lw=1)
        ax.fill_between(pair["wavelength"], -pair["reference_sigma"],
                        pair["reference_sigma"], color="#bd3e0c", alpha=.1,
                        label="± quadrature-error reference")
        ax.plot(pair["wavelength"], pair["difference"], "o", ms=2.1, color="#17212b")
        ax.set_ylabel("Δ depth\n[ppm]")
        ax.set_title(pair["pair"], loc="left", fontsize=9)
        ax.grid(alpha=.18)
    axes[0].legend(frameon=False, fontsize=7, loc="upper right")
    axes[-1].set_xlabel("Reference-grid wavelength [µm]")
    fig.suptitle("Cross-pipeline differences — descriptive because all reductions share one observation",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(AGREEMENT_FIGURE, dpi=200)
    plt.close(fig)
    return {"rows": rows, "pairs": pairs, "n": min(row["n"] for row in rows)}


if __name__ == "__main__":
    result = main()
    print(f"WASP-18 b: four correlated reductions; {result['n']} bins each")
    for pair in result["pairs"]:
        print(f"{pair['pair']}: median |difference|="
              f"{pair['median_absolute_difference_ppm']:.1f} ppm; "
              f"median |independence z|={pair['median_abs_independence_z']:.2f}")
