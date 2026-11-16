# Scientific methods and limitations

WASP-18 b: (1) inverse-variance spectral band-to-continuum contrast and its formal diagonal-error uncertainty, (2) wavelength-window shift sensitivity. Window edges are half-open; each window needs at least two bins. Shared photons, covariance between spectral bins, and alternative reduction dependence are not accounted for. Window choices must be scientifically justified before interpreting observational values. Tests are synthetic. AI-assisted implementation; Biswajit Jana requested as sole Git author/committer. No detection or observational result claimed.

Run: `python -m unittest discover -s tests -p 'test_spectral_robustness.py'`.
