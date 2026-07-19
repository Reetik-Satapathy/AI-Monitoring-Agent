from flask import Flask, request, jsonify
from pydantic import ValidationError

from aikubagent.models.webhook import AlertmanagerWebhook
from aikubagent.services.parser import AlertParser

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "AI Agent is running!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True)

    print("\n========== ALERT RECEIVED ==========", flush=True)

    if payload is None:
        print("No JSON payload received.", flush=True)
        print(f"Content-Type: {request.content_type}", flush=True)
        print(
            f"Raw Body: {request.data.decode('utf-8', errors='ignore')}",
            flush=True,
        )

        return jsonify({
            "status": "error",
            "message": "No JSON payload received"
        }), 400

    try:
        webhook_data  = AlertmanagerWebhook.model_validate(payload)

        # Print the validated Pydantic model
        incidents = AlertParser.parse(webhook_data )

        print(f"Parsed {len(incidents)} incident(s)\n", flush=True)
        
        for incident in incidents:
            print(incident.model_dump_json(indent=4), flush=True)

        print("\n====================================\n", flush=True)

        return jsonify({
            "status": "received"
        }), 200

    except ValidationError as e:
        print("\n===== VALIDATION ERROR =====", flush=True)
        print(e, flush=True)
        print("============================\n", flush=True)

        return jsonify({
            "status": "error",
            "message": "Invalid Alertmanager payload",
            "errors": e.errors()
        }), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )