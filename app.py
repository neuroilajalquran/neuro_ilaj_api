from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# ✅ Allow CORS for all origins (you can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 In production, replace "*" with your frontend domain
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
