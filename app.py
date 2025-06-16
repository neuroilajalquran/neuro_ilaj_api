from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://neuro-ilaj-api.onrender.com"],  # ✅ Your Flutter Web app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
