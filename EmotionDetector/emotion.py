import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time
import cv2
from PIL import Image
import os
import math
import gdown
MODEL_PATH = "Emotion_Detector.h5"
FILE_ID = "1vCrwOvdwGL8YxQXBoPHAdtqKr5X8_hyv"
if not os.path.exists(MODEL_PATH):
    with st.status("🚀 Initializing download...", expanded=True) as status:
        st.write("🔁 Initializing secure model download...")
        time.sleep(1)
        st.write("⬇️ Fetching trained model...")
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", MODEL_PATH, quiet=False)
        time.sleep(1)
        st.write("✅ Model downloaded successfully!")
        status.update(label="✅ All set!", state="complete")
model = load_model(MODEL_PATH)
emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
emoji_map = {
    'angry': "😠", 'disgusted': "🤢", 'fearful': "😨",
    'happy': "😄", 'neutral': "😐", 'sad': "😢", 'surprised': "😲"
}
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def preprocess_image(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        gray = image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face = gray[y:y + h, x:x + w]
    else:
        if gray.shape[0] <= 64 and gray.shape[1] <= 64:
            face = gray
        else:
            return None
    resized = cv2.resize(face, (150, 150))
    rgb_face = np.stack((resized,) * 3, axis=-1).astype('float32') / 255.0
    return np.expand_dims(rgb_face, axis=0)
def predict_emotion(image):
    processed = preprocess_image(np.array(image))
    if processed is None:
        return None, None
    prediction = model.predict(processed, verbose=0)[0]
    confidence = np.max(prediction)
    label = emotions[np.argmax(prediction)]
    return label, confidence
st.set_page_config(page_title="Emotion Detector", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF6F61;'>🧠 Emotion Detector</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #6C757D;'>Upload a face image or try a sample to detect the emotion</h5>", unsafe_allow_html=True)
st.markdown("### 📤 <span style='color:#118AB2'>Upload Your Image</span>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload JPG, JPEG or PNG", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    resized = image.resize((300, 300))
    st.image(resized, caption="Uploaded Image", use_container_width=False)
    label, conf = predict_emotion(image)
    if label is None:
        st.warning("⚠️ No face detected.")
    elif conf < 0.4:
        st.error("❌ Not a known emotion")
    else:
        emoji = emoji_map.get(label, "")
        st.success(f"✅ Detected Emotion: **{label.upper()}** {emoji} — Confidence: `{conf:.2f}`")
st.markdown("### 🖼️ <span style='color:#06D6A0'>Try with Sample Images</span>", unsafe_allow_html=True)
sample_dir = "Samples"
sample_files = sorted([f for f in os.listdir(sample_dir) if f.endswith(('jpg', 'jpeg', 'png'))])
images_per_row = 5
total_images = len(sample_files)
rows = math.ceil(total_images / images_per_row)
for row in range(rows):
    cols = st.columns(images_per_row)
    for i in range(images_per_row):
        idx = row * images_per_row + i
        if idx >= total_images:
            break
        file = sample_files[idx]
        path = os.path.join(sample_dir, file)
        img = Image.open(path).convert("RGB")
        thumb = img.resize((100, 100))
        cols[i].image(thumb, caption=None, width=100)
        if cols[i].button("🔍 Predict", key=f"predict_{file}"):
            st.image(img.resize((300, 300)), caption=f"Sample: {file}", use_container_width=False)
            label, conf = predict_emotion(img)
            if label is None:
                st.warning("⚠️ No face detected.")
            elif conf < 0.4:
                st.error("❌ Not a known emotion")
            else:
                emoji = emoji_map.get(label, "")
                st.success(f"✅ Detected Emotion: **{label.upper()}** {emoji} — Confidence: `{conf:.2f}`")
