from fastapi import FastAPI
from pydantic import BaseModel
import base64

app = FastAPI()

class EEGFile(BaseModel):
    filename: str
    content: str

@app.post("/analyze-eeg")
def analyze_eeg(file: EEGFile):
    decoded = base64.b64decode(file.content)
    text_data = decoded.decode("utf-8")

    # Simple EEG logic: count number of lines
    num_lines = len(text_data.strip().split('\n'))

    return {
        "summary": f"EEG file '{file.filename}' received. Total lines: {num_lines}."
    }
