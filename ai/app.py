from flask import Flask, jsonify, request
import json
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "/app/incidents.log"

def write_log(data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def analyze_alert(name):
    if name == "InstanceDown":
        return {
            "cause": "Servicio detenido o no accesible",
            "severity": "critical",
            "action": "restart node-exporter"
        }

    if name == "HighCPU":
        return {
            "cause": "Proceso consumiendo CPU",
            "severity": "warning",
            "action": "manual review"
        }

    return {
        "cause": "Desconocida",
        "severity": "unknown",
        "action": "manual review"
    }

@app.route("/")
def home():
    return jsonify({"service": "AI Analyzer", "status": "running"})

@app.route("/analyze/<alert_name>")
def analyze(alert_name):
    result = analyze_alert(alert_name)
    return jsonify({"alert": alert_name, **result})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    alerts = data.get("alerts", [])

    responses = []

    for alert in alerts:
        name = alert["labels"]["alertname"]
        result = analyze_alert(name)

        log = {
            "time": datetime.utcnow().isoformat(),
            "alert": name,
            "result": result
        }

        write_log(log)
        responses.append(log)

    return jsonify({"processed": responses})

app.run(host="0.0.0.0", port=5000)
