from flask import Flask, request, jsonify
from pydantic import ValidationError

from aikubagent.models.webhook import AlertmanagerWebhook
from aikubagent.services.parser import AlertParser
from aikubagent.services.analyzer import IncidentAnalyzer
from aikubagent.services.context_builder import ContextBuilder

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
        webhook_data = AlertmanagerWebhook.model_validate(payload)

        incidents = AlertParser.parse(webhook_data)

        print(f"Parsed {len(incidents)} incident(s)\n", flush=True)

        for incident in incidents:

            enriched_incident = ContextBuilder.build(incident)
            enriched_incident = ContextBuilder.build(incident)

            print("\n========== ENRICHED INCIDENT ==========\n", flush=True)

            print(
                enriched_incident.model_dump_json(indent=4),
                flush=True
            )
            analysis = IncidentAnalyzer.analyze(enriched_incident)

            print("\n========== AI ANALYSIS ==========\n", flush=True)

            print(f"Summary   : {analysis.summary}", flush=True)
            print(f"Severity  : {analysis.severity}", flush=True)
            print(f"Impact    : {analysis.impact}\n", flush=True)

            print("Possible Causes:", flush=True)
            for cause in analysis.possible_causes:
                print(f"  • {cause}", flush=True)

            print("\nFirst Troubleshooting Step:", flush=True)
            print(f"  {analysis.first_troubleshooting_step}", flush=True)

            print("\n================================\n", flush=True)

        return jsonify({
            "status": "received"
        }), 200

    except Exception as e:
        print("\n===== CREW ERROR =====", flush=True)
        print(e, flush=True)
        print("======================\n", flush=True)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )