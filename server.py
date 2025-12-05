import os
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import google.generativeai as genai

SERVER_HOST = 'localhost'
SERVER_PORT = 8000

API_KEY_CONFIGURED = False
model = None

try:
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        API_KEY_CONFIGURED = True
        print("Gemini API configured successfully.")
    else:
        print("WARNING: GOOGLE_API_KEY environment variable not set.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def analyze_khmer_sentiment(khmer_text: str):
    logs = []
    def log(msg):
        print(msg)
        logs.append(msg)

    log("="*50)
    log("🔹 Server Status: Received new request from client")
    log("="*50)

    if not API_KEY_CONFIGURED or model is None:
        log("Server Status: API not configured - returning error")
        return {
            "result": "Error: Gemini API not configured on the server.",
            "server_log": "\n".join(logs)
        }

    if not khmer_text or not khmer_text.strip():
        log("Server Status: Empty input received - returning error")
        return {
            "result": "Error: Input text is empty.",
            "server_log": "\n".join(logs)
        }

    log(f"Server Status: Received text for analysis: {khmer_text}")

    prompt = f"""Analyze the sentiment of the following Khmer text.
Consider the nuances of the Khmer language.
Respond with only one single word: 'positive', 'negative', or 'neutral'. Do not add any other explanation or punctuation.

Khmer text: "{khmer_text}"
Sentiment:"""

    try:
        log("Server Status: Processing sentiment analysis with Gemini API...")
        response = model.generate_content(prompt)
        sentiment = response.text.strip().lower()
        log(f"Server Status: Raw API response: {sentiment}")

        if sentiment == "positive":
            result = "មតិវិជ្ជមាន (Positive)"
        elif sentiment == "negative":
            result = "​មតិជាន់ពន្លិច (Negative)"
        elif sentiment == "neutral":
            result = "​មតិធម្មតា (Neutral)"
        else:
            if "positive" in sentiment:
                result = "មតិវិជ្ជមាន (Positive)"
            elif "negative" in sentiment:
                result = "​មតិជាន់ពន្លិច (Negative)"
            elif "neutral" in sentiment:
                result = "​មតិធម្មតា (Neutral)"
            else:
                result = f"Unknown sentiment (LLM response: {response.text.strip()})"

        log(f"Server Status: Analysis complete. Sending response: {result}")

        return {
            "result": result,
            "server_log": "\n".join(logs)
        }

    except Exception as e:
        error_msg = f" Error during sentiment analysis: {str(e)}"
        log(f"Server Status: Error occurred - {error_msg}")
        return {
            "result": error_msg,
            "server_log": "\n".join(logs)
        }

if __name__ == "__main__":
    print(f"Starting XML-RPC server on {SERVER_HOST}:{SERVER_PORT}...")
    print("Awaiting client requests for Khmer sentiment analysis.")
    if not API_KEY_CONFIGURED:
        print("REMINDER: Gemini API is not configured. Sentiment analysis will fail.")

    with SimpleXMLRPCServer((SERVER_HOST, SERVER_PORT),
                            requestHandler=RequestHandler,
                            allow_none=True) as server:
        server.register_introspection_functions()
        server.register_function(analyze_khmer_sentiment, 'analyze_sentiment')
        print(" Function 'analyze_sentiment' registered.")
        print(" Server is ready. Press Ctrl+C to stop.")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n Server shutting down.")
