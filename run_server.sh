#!/bin/bash
uv run --with fastapi,openai,"fastrtc[vad, tts, stt], langchain, langchain-ollama, dotenv, uvicorn" uvicorn app:app --host 0.0.0.0 --port 8000
