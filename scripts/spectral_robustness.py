"""Finite-window contrast and wavelength-mask sensitivity for eclipse spectra."""
import numpy as np

def band_contrast(wavelength, depth, error, band, continuum):
    """Inverse-variance band minus continuum mean, independent-bin errors."""
    w,y,s=map(lambda x:np.asarray(x,dtype=float),(wavelength,depth,error))
    if w.ndim!=1 or len(w)<4 or y.shape!=w.shape or s.shape!=w.shape or not all(np.all(np.isfinite(x)) for x in (w,y,s)) or np.any(s<=0) or np.any(np.diff(w)<=0):
        raise ValueError("sorted finite wavelength, depth, positive errors required")
    if any(len(t)!=2 or not np.all(np.isfinite(t)) or t[0]>=t[1] for t in (band,continuum)) or max(band[0],continuum[0])<min(band[1],continuum[1]):
        raise ValueError("invalid or overlapping windows")
    masks=[(w>=t[0])&(w<t[1]) for t in (band,continuum)]
    if any(m.sum()<2 for m in masks): raise ValueError("each window needs >=2 bins")
    means=[];variances=[]
    for m in masks:
        weights=1/s[m]**2
        means.append(np.sum(weights*y[m])/sum(weights))
        variances.append(1/sum(weights))
    return float(means[0]-means[1]),float(np.sqrt(sum(variances)))

def window_shift_sensitivity(wavelength,depth,error,band,continuum,shifts):
    """Recalculate band contrast for explicitly selected wavelength shifts."""
    shifts=np.asarray(shifts,dtype=float)
    if shifts.ndim!=1 or not np.all(np.isfinite(shifts)):
        raise ValueError("finite one-dimensional shifts required")
    return np.array([band_contrast(wavelength,depth,error,(band[0]+d,band[1]+d),(continuum[0]+d,continuum[1]+d)) for d in shifts]).reshape(-1,2)
