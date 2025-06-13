import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

def process_eeg(file):
    df = pd.read_csv(file)
    data = df['Channel 1']  # Adjust to match your file
    filtered = bandpass_filter(data, 1, 50, 250)
    return {"mean": float(np.mean(filtered)), "std": float(np.std(filtered))}

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)
