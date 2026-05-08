# RPC-SentimentAnalysis

A Khmer-language sentiment analysis system built on **XML-RPC**, with Google's **Gemini** model doing the analysis. It ships with three ways to use it: a CLI client, a Flask web chat UI, or a direct RPC call from your own code.

Built as a coursework project for the Institute of Technology of Cambodia (ITC).

## Architecture

```
+--------------------+        XML-RPC         +-------------------+        HTTPS
|  client.py (CLI)   |  <------------------>  |     server.py     |  <----------->  Google Gemini API
|  Flask app.py      |     localhost:8000     |  (analyze_        |                 (gemini-1.5-flash-latest)
|  Browser UI        |          /RPC2         |   sentiment)      |
+--------------------+                        +-------------------+
```

- **`server.py`** — XML-RPC server. Exposes `analyze_sentiment(text)`, which prompts Gemini and returns one of *positive / negative / neutral* (translated into Khmer).
- **`client.py`** — Interactive CLI client. Type Khmer text, get a sentiment label.
- **`khmer_sentiment_frontend/app.py`** — Flask web app. Bridges browser ⇄ XML-RPC server and renders a chat-style UI with a live "RPC terminal" view.

## Requirements

- Python 3.10+
- A Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- Packages: `google-generativeai`, `flask`

```bash
pip install google-generativeai flask
```

## Setup

Set your Gemini API key as an environment variable.

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "your_api_key_here"
```

**macOS / Linux:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Usage

### 1. Start the XML-RPC server

In one terminal:

```bash
python server.py
```

The server listens on `http://localhost:8000/RPC2`.

### 2a. Use the CLI client

In another terminal:

```bash
python client.py
```

Then enter Khmer text at the prompt. Type `exit` to quit.

### 2b. Use the web frontend

In another terminal:

```bash
cd khmer_sentiment_frontend
python app.py
```

Open `http://localhost:5000` in your browser. Type Khmer text into the chat box; the sentiment result appears as a bot reply, and the right-hand "RPC Process" panel shows the round-trip server log.

## Project Structure

```
RPC-SentimentAnalysis/
├── server.py                          # XML-RPC server (Gemini-powered)
├── client.py                          # Interactive CLI client
├── khmer_sentiment_frontend/
│   ├── app.py                         # Flask app bridging browser <-> RPC server
│   ├── templates/index.html           # Chat UI
│   └── static/
│       ├── css/style.css
│       ├── js/script.js
│       └── images/                    # ITC logo, etc.
└── README.md
```

## RPC API

A single remote procedure is registered:

**`analyze_sentiment(khmer_text: str) -> dict`**

Returns:
```python
{
    "result": "មតិវិជ្ជមាន (Positive)" | "​មតិជាន់ពន្លិច (Negative)" | "​មតិធម្មតា (Neutral)" | "Error: ...",
    "server_log": "<multi-line server-side log of this call>"
}
```

Example call from any Python program:
```python
import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
print(proxy.analyze_sentiment("ខ្ញុំសប្បាយចិត្តណាស់ថ្ងៃនេះ"))
```

## Notes

- The server logs a warning and returns an error from `analyze_sentiment` if `GOOGLE_API_KEY` isn't set when it starts.
- The Flask frontend assumes the XML-RPC server is reachable at `http://localhost:8000/RPC2` — adjust `rpc_client` in `khmer_sentiment_frontend/app.py` if you change the host or port.
- Both the CLI and web frontend require the XML-RPC server (`server.py`) to be running first.
