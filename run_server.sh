#!/bin/bash
uv run --with fastapi,openai,"fastrtc[vad, tts, stt]" uvicorn app:app --host 0.0.0.0 --port 8000
