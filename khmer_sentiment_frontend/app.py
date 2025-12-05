from flask import Flask, render_template, request, jsonify
import xmlrpc.client

app = Flask(__name__)

# Connect to XML-RPC server at the /RPC2 path!
rpc_client = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_sentiment", methods=["POST"])
def get_sentiment():
    data = request.get_json()
    text = data.get("text", "")

    try:
        response = rpc_client.analyze_sentiment(text)

        if isinstance(response, str):
            # fallback if server returned plain string
            return jsonify({
                "response": response,
                "server_log": ""
            })

        return jsonify({
            "response": response.get("result", "No result"),
            "server_log": response.get("server_log", "")
        })
    except Exception as e:
        return jsonify({
            "response": f"Error contacting RPC server: {str(e)}",
            "server_log": ""
        })

if __name__ == "__main__":
    app.run(debug=True)