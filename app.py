# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastapi",
#     "fastrtc[stt,tts,vad]",
#     "openai",
#     "python-dotenv",
#     "uvicorn",
# ]
# ///
from fastrtc import (ReplyOnPause, Stream, AdditionalOutputs,
                     get_stt_model, get_tts_model)
from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")

llm_client = OpenAI(
    api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL
)
stt_model = get_stt_model()
tts_model = get_tts_model()


def talk(audio, chat_history):
    prompt = stt_model.stt(audio)
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)
    response = llm_client.chat.completions.create(
        model=OPENAI_MODEL,  # Update based on your LLM / Agent
        messages=chat_history,
        max_tokens=200,
    )
    yield AdditionalOutputs(json.dumps(user_message))
    ai_reply = response.choices[0].message.content
    ai_response = {"role": "ai", "content": ai_reply}
    chat_history.append(ai_response)
    yield AdditionalOutputs(json.dumps(ai_response))
    for audio_chunk in tts_model.stream_tts_sync(ai_reply):
        yield audio_chunk


stream = Stream(ReplyOnPause(talk), modality="audio", mode="send-receive")

app = FastAPI()
stream.mount(app)

app.mount("/static", StaticFiles(directory="static"))

# Optional: Add routes


@app.get("/")
async def _():
    return HTMLResponse(content=open("index.html").read())


class InputData(BaseModel):
    webrtc_id: str
    chatbot: List[dict] = []


@app.post("/input_hook")
async def _(data: InputData):
    stream.set_input(data.webrtc_id, data.chatbot)


@app.get("/outputs")
async def stream_updates(webrtc_id: str):
    async def output_stream():
        async for output in stream.output_stream(webrtc_id):
            # Output is the AdditionalOutputs instance
            # Be sure to serialize it however you would like
            yield f"data: {output.args[0]}\n\n"

    return StreamingResponse(
        output_stream(),
        media_type="text/event-stream"
    )
# uvicorn app:app --host 0.0.0.0 --port 8000
