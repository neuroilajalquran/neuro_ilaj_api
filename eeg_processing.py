import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

# Band definitions in Hz
DELTA_BAND = (0.5, 4)
THETA_BAND = (4, 8)
ALPHA_BAND = (8, 13)
BETA_BAND = (13, 30)

SAMPLING_RATE = 256  # Hz, adjust if needed

def bandpass_filter(data, lowcut, highcut, fs=SAMPLING_RATE, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def band_power(signal, band):
    freqs = np.fft.rfftfreq(len(signal), d=1.0 / SAMPLING_RATE)
    fft_values = np.abs(np.fft.rfft(signal)) ** 2
    idx = np.where((freqs >= band[0]) & (freqs <= band[1]))
    return np.sum(fft_values[idx])

def process_eeg(file):
    df = pd.read_csv(file)

    # Detect EEG columns (assumes format: Time, Ch1, Ch2, ..., Ch8)
    eeg_columns = [col for col in df.columns if 'Channel' in col or 'Ch' in col]

    results = {}

    for ch in eeg_columns:
        signal = df[ch].dropna().values

        # Optional: apply bandpass filter to remove noise
        signal = bandpass_filter(signal, 0.5, 45)

        delta = band_power(signal, DELTA_BAND)
        theta = band_power(signal, THETA_BAND)
        alpha = band_power(signal, ALPHA_BAND)
        beta = band_power(signal, BETA_BAND)
        total = delta + theta + alpha + beta

        alpha_beta_ratio = alpha / beta if beta else 0

        results[ch] = {
            "delta": float(delta),
            "theta": float(theta),
            "alpha": float(alpha),
            "beta": float(beta),
            "alpha_beta_ratio": round(alpha_beta_ratio, 4),
            "relative_power": {
                "delta": round(delta / total * 100, 2) if total else 0,
                "theta": round(theta / total * 100, 2) if total else 0,
                "alpha": round(alpha / total * 100, 2) if total else 0,
                "beta": round(beta / total * 100, 2) if total else 0,
            }
        }

    return results
