from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/analyze-eeg/")
async def analyze_eeg(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Example: Basic filtering
    result = {
        "mean_per_channel": df.mean().to_dict(),
        "max_per_channel": df.max().to_dict()
    }

    return result
