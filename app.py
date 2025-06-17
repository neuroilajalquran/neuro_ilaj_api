from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body model
class EEGRequest(BaseModel):
    filename: str
    content: str

# ✅ Frequency band ranges (in Hz)
DELTA_BAND = (0.5, 4)
THETA_BAND = (4, 8)
ALPHA_BAND = (8, 13)
BETA_BAND  = (13, 30)

# ✅ Assume 256 Hz sampling rate
SAMPLING_RATE = 256.0

@app.post("/analyze-eeg")
def analyze_eeg(data: EEGRequest):
    try:
        lines = data.content.strip().splitlines()

        channel_data = [[] for _ in range(8)]  # 8 EEG channels

        for line in lines:
            if line.startswith('%'):
                continue  # Skip header lines

            parts = line.strip().split(',')
            if len(parts) >= 9:
                try:
                    for i in range(8):
                        channel_data[i].append(float(parts[i + 1]))
                except ValueError:
                    continue

        if not any(channel_data):
            return {"error": "No valid EEG data found."}

        def band_power(signal, band):
            freqs = np.fft.rfftfreq(len(signal), d=1.0/SAMPLING_RATE)
            fft_values = np.abs(np.fft.rfft(signal)) ** 2
            idx = np.where((freqs >= band[0]) & (freqs <= band[1]))
            return np.sum(fft_values[idx])

        results = {}
        for i, signal in enumerate(channel_data):
            signal = np.array(signal)
            if len(signal) < 2:
                continue

            delta_power = band_power(signal, DELTA_BAND)
            theta_power = band_power(signal, THETA_BAND)
            alpha_power = band_power(signal, ALPHA_BAND)
            beta_power  = band_power(signal, BETA_BAND)
            total_power = delta_power + theta_power + alpha_power + beta_power

            alpha_beta_ratio = alpha_power / beta_power if beta_power != 0 else 0.0

            results[f"Channel_{i+1}"] = {
                "delta": float(delta_power),
                "theta": float(theta_power),
                "alpha": float(alpha_power),
                "beta": float(beta_power),
                "alpha_beta_ratio": round(alpha_beta_ratio, 4),
                "relative_power": {
                    "delta": round(delta_power / total_power * 100, 2) if total_power else 0.0,
                    "theta": round(theta_power / total_power * 100, 2) if total_power else 0.0,
                    "alpha": round(alpha_power / total_power * 100, 2) if total_power else 0.0,
                    "beta":  round(beta_power / total_power * 100, 2) if total_power else 0.0,
                }
            }

        return {"analysis": results}

    except Exception as e:
        return {"error": str(e)}
