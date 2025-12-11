from flask import Flask, request, jsonify
import json
import hashlib

app = Flask(__name__)

# Nếu SeaTalk có cung cấp Signing Secret, dán vào đây:
SIGNING_SECRET = b""  # ví dụ: b"1234567812345678"

def is_valid_signature(body: bytes, signature: str) -> bool:
    if not SIGNING_SECRET:
        return True
    if not signature:
        return False
    return hashlib.sha256(body + SIGNING_SECRET).hexdigest() == signature

@app.route("/", methods=["GET"])
def index():
    return "SeaTalk callback server is running.", 200

@app.route("/bot-callback", methods=["POST"])
def bot_callback():
    body_bytes = request.get_data()
    signature = request.headers.get("signature", "")
    
    if not is_valid_signature(body_bytes, signature):
        return "Invalid signature", 403

    data = json.loads(body_bytes)
    event_type = data.get("event_type")

    # Xử lý bước xác minh URL
    if event_type == "event_verification":
        challenge = data["event"]["seatalk_challenge"]
        return jsonify({"seatalk_challenge": challenge}), 200

    # In ra log để xem sự kiện
    print("Received event:", data)

    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
