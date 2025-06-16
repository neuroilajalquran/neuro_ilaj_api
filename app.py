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
        values = [float(x.strip()) for x in data.content.split(",")]
        mean_val = float(np.mean(values))
        std_val = float(np.std(values))
        return {"mean": mean_val, "std": std_val}
    except Exception as e:
        return {"error": str(e)}
