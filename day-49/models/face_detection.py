#!/usr/bin/env python3
"""
day-49/models/face_detection.py

Detect faces in images using OpenCV’s Haar cascades. If the cascade
XML isn’t installed, this script will download it from the OpenCV GitHub
and cache it locally.
"""

import os
import cv2
import urllib.request
import sys

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR    = os.path.dirname(__file__)
DAY_DIR       = os.path.dirname(SCRIPT_DIR)
CACHE_DIR     = os.path.join(SCRIPT_DIR, "cascade_cache")
LOCAL_CASCADE = os.path.join(CACHE_DIR, "haarcascade_frontalface_default.xml")

# ─── Cascade Download Info ───────────────────────────────────────────────────
CASCADE_URL = (
    "https://raw.githubusercontent.com/opencv/opencv/master/"
    "data/haarcascades/haarcascade_frontalface_default.xml"
)

def ensure_cascade():
    os.makedirs(CACHE_DIR, exist_ok=True)
    if os.path.exists(LOCAL_CASCADE):
        return LOCAL_CASCADE

    print(f"Cascade not found locally. Downloading to {LOCAL_CASCADE}…")
    try:
        urllib.request.urlretrieve(CASCADE_URL, LOCAL_CASCADE)
    except Exception as e:
        print("❌ Failed to download cascade:", e)
        sys.exit(1)
    print("✅ Cascade downloaded.")
    return LOCAL_CASCADE

# ─── Initialize Cascade ──────────────────────────────────────────────────────
cascade_path = ensure_cascade()
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print("❌ Failed to load cascade classifier from", cascade_path)
    sys.exit(1)

# ─── Directories ─────────────────────────────────────────────────────────────
FACE_DIR   = os.path.join(DAY_DIR, "faces")    # your folder of input images
OUTPUT_DIR = os.path.join(DAY_DIR, "plots")    # where to write outputs
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Face Detection ───────────────────────────────────────────────────────────
def detect_and_draw(in_path, out_path):
    img = cv2.imread(in_path)
    if img is None:
        print("⚠️  Could not read:", in_path)
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imwrite(out_path, img)
    print(f"Saved `{out_path}` — {len(faces)} face(s) detected.")

def main():
    for fname in os.listdir(FACE_DIR):
        if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
            continue
        in_file  = os.path.join(FACE_DIR, fname)
        out_file = os.path.join(OUTPUT_DIR, f"detection_{fname}")
        detect_and_draw(in_file, out_file)

if __name__ == "__main__":
    main()
