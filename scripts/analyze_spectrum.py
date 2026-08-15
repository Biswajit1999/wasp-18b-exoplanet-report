from __future__ import annotations
import csv
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

def flat_test(values, errors):
    values, errors = np.asarray(values, float), np.asarray(errors, float)
    good = np.isfinite(values) & np.isfinite(errors) & (errors > 0)
    values, errors = values[good], errors[good]
    weights = 1 / errors**2
    mean = np.sum(weights * values) / np.sum(weights)
    statistic = np.sum(((values - mean) / errors)**2)
    dof = len(values) - 1
    return {"n": len(values), "mean": mean, "chi2": statistic, "dof": dof,
            "p": chi2.sf(statistic, dof)}

def offset_model_test(wavelength, values, errors, model_wavelength, model_values):
    model = np.interp(wavelength, model_wavelength, model_values)
    weights = 1 / errors**2
    offset = np.sum(weights * (values - model)) / np.sum(weights)
    statistic = np.sum(((values - model - offset) / errors)**2)
    dof = len(values) - 1
    return {"n": len(values), "offset": offset, "chi2": statistic,
            "dof": dof, "p": chi2.sf(statistic, dof), "model": model + offset}

def write_rows(rows):
    fields = sorted({key for row in rows for key in row})
    with STATS_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)

FIGURE_FILE = FIGURES / "wasp18b_published_spectrum.png"

def binned(wavelength, values, errors, width=.04):
    edges = np.arange(wavelength.min(), wavelength.max() + width, width)
    x, y, e = [], [], []
    for left, right in zip(edges[:-1], edges[1:]):
        use = (wavelength >= left) & (wavelength < right)
        if not use.any(): continue
        weights = 1 / errors[use]**2
        x.append(np.sum(weights * wavelength[use]) / np.sum(weights))
        y.append(np.sum(weights * values[use]) / np.sum(weights))
        e.append(np.sqrt(1 / np.sum(weights)))
    return np.asarray(x), np.asarray(y), np.asarray(e)

def main():
    FIGURES.mkdir(exist_ok=True); rows = []
    fig, ax = plt.subplots(figsize=(9.2, 5.3))
    for path in sorted(DATA.glob("*_w18b_spectrum.txt")):
        values = np.loadtxt(path); label = path.stem.replace("_w18b_spectrum", "")
        result = flat_test(values[:, 1], values[:, 2]); rows.append({"comparison": label + " vs weighted flat", **result})
        x, y, e = binned(values[:, 0], values[:, 1], values[:, 2])
        ax.errorbar(x, y, yerr=e, fmt="o-", ms=3, lw=1, alpha=.72, label=label)
    write_rows(rows)
    ax.set(xlabel="Wavelength [micron]", ylabel="Planet/star flux ratio [ppm]",
           title="WASP-18 b: four published JWST NIRISS/SOSS eclipse reductions")
    ax.grid(alpha=.2); ax.legend(frameon=False, fontsize=8); fig.tight_layout()
    fig.savefig(FIGURE_FILE, dpi=190); plt.close(fig)
    return {"rows": rows, "n": min(row["n"] for row in rows)}

if __name__ == "__main__":
    result = main(); print(f"WASP-18 b: four reductions; at least {result['n']} bins each")
