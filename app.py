from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class EEGRequest(BaseModel):
    filename: str
    content: str

@app.post("/analyze-eeg")
def analyze_eeg(data: EEGRequest):
    try:
        lines = data.content.strip().splitlines()

        eeg_values = []

        for line in lines:
            if line.startswith('%'):
                continue  # Skip headers

            parts = line.strip().split(',')

            # Extract EEG channels (index 1 to 8)
            if len(parts) >= 9:
                try:
                    values = [float(parts[i]) for i in range(1, 9)]
                    eeg_values.extend(values)
                except ValueError:
                    continue  # Skip rows with invalid data

        if not eeg_values:
            return {"error": "No valid EEG data found."}

        mean_val = float(np.mean(eeg_values))
        std_val = float(np.std(eeg_values))

        return {"mean": mean_val, "std": std_val}

    except Exception as e:
        return {"error": str(e)}
