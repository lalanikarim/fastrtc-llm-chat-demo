# Real-Time Voice Chatbot with FastRTC

This project demonstrates a real-time voice chatbot built using Python, FastAPI, and the FastRTC library. It captures user audio via WebRTC, transcribes it using Speech-to-Text (STT), sends the text to a Large Language Model (LLM) for a response, synthesizes the response using Text-to-Speech (TTS), and streams the audio back to the user through a web interface.

## Features

*   **Real-time Audio Streaming:** Bidirectional audio communication using WebRTC.
*   **Voice Activity Detection (VAD):** Uses FastRTC's `ReplyOnPause` to automatically detect when the user stops speaking.
*   **Speech-to-Text (STT):** Transcribes the user's speech into text.
*   **LLM Integration:** Connects to an OpenAI-compatible API endpoint (defaults to Ollama) to generate conversational responses.
*   **Text-to-Speech (TTS):** Synthesizes the LLM's text response into audio.
*   **Web Interface:** Provides a simple HTML/CSS/JS frontend (`index.html`) for interaction, including audio visualization and chat history display.

## Requirements

*   Python 3.10 or higher.
*   `pip` for installing Python packages. (`uv` is used in `run_server.sh` but `pip` works too).
*   An accessible LLM endpoint compatible with the OpenAI API. The code defaults to Ollama running at `http://aurora:11434/v1`.
    *   You need the LLM server (e.g., Ollama) running and accessible from where you run the Python application.
    *   The specific model (`llama3.2` in the code) must be available on the LLM server.
*   A modern web browser supporting WebRTC and microphone access (e.g., Chrome, Firefox, Edge).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lalanikarim/fastrtc-llm-chat-demo.git
    cd fastrtc-llm-chat-demo
    ```

2.  **Install Python dependencies:**
    You can use `pip` (or `uv` if you have it installed):
    ```bash
    pip install fastapi openai "fastrtc[vad,tts,stt]" uvicorn
    ```
    *Note: The `run_server.sh` script uses `uv` to manage dependencies and run the server, which might handle installation automatically if `uv` is present.*

## Configuration

1.  **LLM Endpoint:**
    The application connects to an LLM specified in `app.py`:
    ```python
    llm_client = OpenAI(
        api_key="ollama", base_url="http://aurora:11434/v1"
    )
    # ... uses model="llama3.2" later
    ```
    *   Ensure your LLM server (e.g., Ollama) is running.
    *   Verify that the `base_url` (`http://aurora:11434/v1`) is correct for your setup. Replace `aurora` with `localhost` or the appropriate IP/hostname if needed.
    *   Make sure the model specified (`llama3.2`) is available on your LLM server (e.g., run `ollama pull llama3.2` if using Ollama).
    *   The `api_key="ollama"` is standard when using Ollama's OpenAI compatibility endpoint. Adjust if your endpoint requires a different key.

## Running the Application

You can run the application using the provided shell script or directly with `uvicorn`.

1.  **Using the script (Recommended):**
    Make sure the script is executable (`chmod +x run_server.sh`) and then run:
    ```bash
    ./run_server.sh
    ```
    This script uses `uv` to run `uvicorn` with the necessary dependencies enabled.

2.  **Using uvicorn directly:**
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```
    Ensure you have installed all dependencies as mentioned in the Installation section.

The server will start, typically listening on `http://0.0.0.0:8000`.

## Usage

1.  Open your web browser and navigate to `http://localhost:8000` (or the IP address of the server if running remotely).
2.  Click the "Start" button.
3.  Your browser will likely ask for permission to access your microphone. Grant permission.
4.  The button should change to "Connecting..." and then "Stop" with a pulsing indicator once connected.
5.  Speak clearly into your microphone. When you pause, the application will:
    *   Transcribe your speech (displayed as a "user" message).
    *   Show a "typing indicator".
    *   Send the transcription to the LLM.
    *   Receive the response from the LLM.
    *   Hide the typing indicator.
    *   Display the LLM's response (as an "assistant" message).
    *   Play the synthesized audio response through your speakers/headphones.
6.  The conversation history is displayed in the chat area.
7.  Click the "Stop" button to disconnect and end the session.

## Technologies Used

*   Python
*   FastAPI
*   FastRTC
*   OpenAI Python Client (for LLM interaction)
*   Uvicorn (ASGI server)
*   WebRTC
*   HTML, CSS, JavaScript
