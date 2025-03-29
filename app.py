# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastapi",
#     "fastrtc[stt,tts,vad]",
#     "openai",
# ]
# ///
import os

from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

sambanova_client = OpenAI(
    api_key="ollama", base_url="http://aurora:11434/v1"
)
stt_model = get_stt_model()
tts_model = get_tts_model()


def echo(audio):
    prompt = stt_model.stt(audio)
    response = sambanova_client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    prompt = response.choices[0].message.content
    for audio_chunk in tts_model.stream_tts_sync(prompt):
        yield audio_chunk


stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")

app = FastAPI()
stream.mount(app)

# Optional: Add routes


@app.get("/")
async def _():
    return HTMLResponse(content=open("index.html").read())

# uvicorn app:app --host 0.0.0.0 --port 8000
