from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from datetime import datetime

from trace import generate_trace_id

app = FastAPI()

# Load dataset
with open("traffic.json", "r") as file:
    raw_data = json.load(file)

# Normalize signals
def build_signals():
    signals = []

    for item in raw_data:
        signal = {
            "trace_id": generate_trace_id(),
            "zone_id": item["zone_id"],
            "domain": item["domain"],
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "traffic_density": item["traffic_density"],
                "violations": item["violations"]
            }
        }

        print("Signal generated →", signal["trace_id"], "→", signal)

        signals.append(signal)

    return signals


# GET /signals
@app.get("/signals")
def get_signals():
    return build_signals()


# GET /signal?zone_id=...
@app.get("/signal")
def get_signal(zone_id: str):
    signals = build_signals()

    for signal in signals:
        if signal["zone_id"] == zone_id:
            return signal

    return JSONResponse(
        status_code=400,
        content={
            "error": "INVALID_ZONE",
            "trace_id": generate_trace_id()
        }
    )