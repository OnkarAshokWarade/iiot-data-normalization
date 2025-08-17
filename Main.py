import json
from datetime import datetime

# Convert ISO timestamp (e.g. 2023-08-17T14:52:00Z) → epoch ms
def iso_to_millis(iso_str: str) -> int:
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)

# Normalize records from data-1.json
def normalize_from_data1(rec: dict) -> dict:
    return {
        "deviceId": rec.get("deviceId") or rec.get("device_id"),
        "timestamp": iso_to_millis(rec["timestamp"]),
        "metric": rec["metric"],
        "value": float(rec["value"])
    }

# Normalize records from data-2.json
def normalize_from_data2(rec: dict) -> dict:
    ts = rec.get("timestamp") or rec.get("ts")
    if isinstance(ts, str):
        ts = iso_to_millis(ts)
    return {
        "deviceId": rec.get("deviceId") or rec.get("device_id"),
        "timestamp": int(ts),
        "metric": rec["metric"],
        "value": float(rec["value"])
    }

# Merge both datasets into one unified list
def unify_all(data1, data2):
    result = [normalize_from_data1(r) for r in data1] + \
             [normalize_from_data2(r) for r in data2]
    result.sort(key=lambda x: x["timestamp"])
    return result

if __name__ == "__main__":   # ✅ fixed here
    # Load JSON files
    with open("data-1.json", "r") as f:
        data1 = json.load(f)

    with open("data-2.json", "r") as f:
        data2 = json.load(f)

    # Transform & unify
    unified = unify_all(data1, data2)

    # Print to console
    print(json.dumps(unified, indent=2))

    # Save to data-result.json
    with open("data-result.json", "w") as f:
        json.dump(unified, f, indent=2)   # ✅ fixed here
