"""Integrity checks for immutable scientific inputs."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "data/tess2018234235059-s0002-0000000100100827-0121-s_lc.fits": "9e83d10406a7ee0274409cd19f39857abbadfbe907e0a1f033d18c00136b0c7b",
    "data/spectra/nirhiss_w18b_spectrum.txt": "8759cb499d0a2dea2df6ec79ea22fa7b544b81c4700595aebdf02ad2cff5c9ea",
    "data/spectra/nameless_w18b_spectrum.txt": "8ee921d8e714b1267539cae0844c9b10b466dc02ed95d9f2ed56028dd2733653",
    "data/spectra/transitspectroscopy_w18b_spectrum.txt": "ed353b9486a60791099d9a8bb2b8bd6ed21065afab6ea8418e14287394671428",
    "data/spectra/supreme_spoon_w18b_spectrum.txt": "779287b7d9f6423b3f4c145a8144890cc43317827e675393251f703488d46377",
}


def digest(path):
    data = path.read_bytes()
    if path.suffix == ".txt":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def test_scientific_inputs_match_documented_checksums():
    for relative, expected in EXPECTED.items():
        assert digest(ROOT / relative) == expected
