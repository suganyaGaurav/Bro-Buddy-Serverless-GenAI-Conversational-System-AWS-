from flask import Flask, render_template, request, jsonify
import requests
import logging

# =========================
# App Initialization
# =========================
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

logging.basicConfig(level=logging.INFO)

# =========================
# CONFIG
# =========================
API_GATEWAY_URL = "https://stpamnah50.execute-api.us-east-1.amazonaws.com/dev/chat"

SUPPORTED_MODES = {"chill", "professional"}

# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    query = data.get("query", "").strip()
    mode = data.get("mode", "professional").lower()

    if not query:
        return jsonify({"answer": "Please enter a message."})

    if mode not in SUPPORTED_MODES:
        mode = "professional"

    payload = {
        "query": query,
        "mode": mode
    }

    try:
        response = requests.post(
            API_GATEWAY_URL,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        app.logger.error(f"Backend error: {e}")
        return jsonify({
            "answer": "Backend error. Please try again later."
        }), 500


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    app.run(debug=True)
