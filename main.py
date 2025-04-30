from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np
import soundfile as sf
import nemo.collections.asr as nemo_asr
import tempfile
import shutil
import os

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize ASR model
asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained("nvidia/stt_en_citrinet_1024_gamma_0_25")
asr_model.to(device)


# Preprocess the audio file
def preprocess_audio(file_path: str) -> str:
    audio, sr = sf.read(file_path)
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)
    processed_file = 'processed_audio.wav'
    sf.write(processed_file, audio, sr)
    return processed_file


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    processed_file = preprocess_audio(temp_file_path)

    try:
        # Perform transcription
        text_generated = asr_model.transcribe([processed_file])
    finally:
        # Clean up temporary files
        os.remove(temp_file_path)
        os.remove(processed_file)

    return {"transcription": text_generated[0]}
