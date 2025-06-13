from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Neuro Ilaj EEG API running!"}

@app.post("/analyze/")
def analyze_eeg(data: dict):
    # Sample EEG processing
    df = pd.DataFrame(data)
    result = df.mean().to_dict()
    return {"result": result}
