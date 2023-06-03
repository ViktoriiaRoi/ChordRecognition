import numpy as np
from scipy import signal

def smooth_signal(X, filt_len=41, down_sampling=10):
    filt_kernel = signal.windows.boxcar(filt_len)[np.newaxis, :]
    X_smooth = signal.convolve(X, filt_kernel, mode='same') / filt_len
    X_smooth = X_smooth[:, ::down_sampling]
    return X_smooth
