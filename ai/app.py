from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"service": "AI Analyzer", "status": "running"})

@app.route("/analyze/<alert_name>")
def analyze(alert_name):
    responses = {
        "InstanceDown": {
            "cause": "Servicio detenido o no accesible",
            "severity": "critical",
            "action": "Revisar contenedor y reiniciar servicio"
        },
        "HighCPU": {
            "cause": "Proceso consumiendo CPU",
            "severity": "warning",
            "action": "Inspeccionar procesos y capacidad"
        }
    }

    result = responses.get(alert_name, {
        "cause": "Desconocida",
        "severity": "unknown",
        "action": "Revisión manual"
    })

    return jsonify({
        "alert": alert_name,
        **result
    })

app.run(host="0.0.0.0", port=5000)
