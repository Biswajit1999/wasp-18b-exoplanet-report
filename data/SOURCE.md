# Data sources

## TESS light curve

- File: `tess2018234235059-s0002-0000000100100827-0121-s_lc.fits`
- Archive: Mikulski Archive for Space Telescopes (MAST), TESS SPOC light-curve product
- TESS sector: 2
- TIC target ID: 100100827
- MAST observation ID: 60867790
- MAST data URI: `mast:TESS/product/tess2018234235059-s0002-0000000100100827-0121-s_lc.fits`
- Exact download URL: <https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:TESS%2Fproduct%2Ftess2018234235059-s0002-0000000100100827-0121-s_lc.fits>
- Collection DOI: [10.17909/t9-nmc8-f686](https://doi.org/10.17909/t9-nmc8-f686) (TESS 2-minute light curves, all sectors; sector 2 used here)
- Retrieved: 2026-08-15
- SHA-256: `9e83d10406a7ee0274409cd19f39857abbadfbe907e0a1f033d18c00136b0c7b`

The FITS file is stored unmodified. The analysis reads `TIME`, `PDCSAP_FLUX`,
`PDCSAP_FLUX_ERR`, and `QUALITY`. PDCSAP flux is the SPOC light curve with common
instrumental trends removed and aperture/crowding corrections applied; this does
not make it free of residual stellar or instrumental systematics.

## System parameters

- File: `system_parameters.csv`
- Service: NASA Exoplanet Archive TAP, `pscomppars` table
- Exact query: <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name%2Chostname%2Cra%2Cdec%2Cpl_orbper%2Cpl_tranmid%2Cpl_trandur%2Cpl_rade%2Cpl_bmasse%2Cpl_eqt%2Cpl_orbsmax%2Csy_dist%2Csy_tmag%2Cst_teff%2Cst_rad%2Cst_mass%2Cdisc_year%2Cdiscoverymethod%2Cdisc_refname%2Cdisc_pubdate%2Cdisc_facility+from+pscomppars+where+pl_name%3D%27WASP-18+b%27&format=csv>
- Retrieved: 2026-08-15

The saved row is the input actually used by `scripts/analyze_transit.py`; the
analysis does not query a changing live service at run time.


## Additional TESS sectors for robustness analysis

All are unmodified standard-cadence SPOC light curves from the same [MAST TESS collection](https://doi.org/10.17909/t9-nmc8-f686).

- Sector 2: `tess2018234235059-s0002-0000000100100827-0121-s_lc.fits` (2,004,480 bytes)
  - MAST URI: `mast:TESS/product/tess2018234235059-s0002-0000000100100827-0121-s_lc.fits`
  - SHA-256: `9e83d10406a7ee0274409cd19f39857abbadfbe907e0a1f033d18c00136b0c7b`

## Published planetary spectrum

- Archive record: [10.5281/zenodo.7907569](https://zenodo.org/records/7907569)
- Data type: emission; instrument: JWST NIRISS/SOSS
- `data/spectra/nirhiss_w18b_spectrum.txt` — SHA-256 `8759cb499d0a2dea2df6ec79ea22fa7b544b81c4700595aebdf02ad2cff5c9ea`
- `data/spectra/nameless_w18b_spectrum.txt` — SHA-256 `8ee921d8e714b1267539cae0844c9b10b466dc02ed95d9f2ed56028dd2733653`
- `data/spectra/transitspectroscopy_w18b_spectrum.txt` — SHA-256 `ed353b9486a60791099d9a8bb2b8bd6ed21065afab6ea8418e14287394671428`
- `data/spectra/supreme_spoon_w18b_spectrum.txt` — SHA-256 `779287b7d9f6423b3f4c145a8144890cc43317827e675393251f703488d46377`
