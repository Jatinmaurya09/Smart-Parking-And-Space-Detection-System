"""
Smart Parking - Flask backend for Vercel deployment.
"""

from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import json
import base64
import os

app = Flask(__name__)


def load_slots(json_path):
    if not os.path.exists(json_path):
        return None
    with open(json_path, 'r') as f:
        return json.load(f)


def is_slot_occupied(image, slot):
    """True = occupied (RED), False = free (GREEN)."""
    x, y, w, h = slot
    mx = int(w * 0.20)
    my = int(h * 0.20)
    x1, y1 = x + mx, y + my
    x2, y2 = x + w - mx, y + h - my
    if x2 <= x1 or y2 <= y1:
        return False

    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return False

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    V = float(np.median(hsv[:, :, 2]))
    S = float(np.median(hsv[:, :, 1]))
    gray_std = float(np.std(gray))

    if V > 195:
        return True
    if V < 100:
        return True
    if S > 55:
        return True
    if gray_std > 45 and V < 180:
        return True
    return False


def process_image(img, slots):
    """Draw rectangles and count occupied/free."""
    occupied = 0
    for slot in slots:
        occ = is_slot_occupied(img, slot)
        x, y, w, h = slot
        if occ:
            occupied += 1
            col = (0, 0, 255)
        else:
            col = (0, 255, 0)
        cv2.rectangle(img, (x, y), (x + w, y + h), col, 3)

    free = len(slots) - occupied
    return img, occupied, free


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        slots_key = request.form.get("slots", "slots_1.json")

        # Read image
        img_bytes = file.read()
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image"}), 400

        slots = load_slots(slots_key)
        if slots is None:
            return jsonify({"error": f"{slots_key} not found"}), 400

        # Process
        img, occupied, free = process_image(img, slots)

        # Encode result as base64
        _, buffer = cv2.imencode(".png", img)
        img_b64 = base64.b64encode(buffer).decode("utf-8")

        return jsonify({
            "total": len(slots),
            "occupied": occupied,
            "free": free,
            "result_image": f"data:image/png;base64,{img_b64}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel entrypoint
handler = app


if __name__ == "__main__":
    app.run(debug=True, port=5000)