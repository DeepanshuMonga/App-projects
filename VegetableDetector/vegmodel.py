import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import math
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time
import gdown
MODEL_PATH = "DetectVegetables.keras"
FILE_ID = "1NXiQ74i-oykIpZ6aqMwxMqDX1Ian4lA_"
if not os.path.exists(MODEL_PATH):
    with st.status("🚀 Initializing download...", expanded=True) as status:
        st.write("🔁 Initializing secure model download...")
        time.sleep(1)
        st.write("⬇️ Fetching trained model...")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False, fuzzy=True, use_cookies=False)
        time.sleep(1)
        st.write("✅ Model downloaded successfully!")
        status.update(label="✅ All set!", state="complete")
model = load_model(MODEL_PATH)
vegetable_classes = [
    'Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Broccoli', 'Cabbage', 'Capsicum', 'Carrot',
    'Cauliflower', 'Cucumber', 'Potato', 'Green Pumpkin', 'Radish', 'Tomato'
]
def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img).astype('float32') / 255.0
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
    return np.expand_dims(img_array, axis=0)
def predict_vegetable(image):
    processed = preprocess_image(image)
    prediction = model.predict(processed, verbose=0)[0]
    confidence = np.max(prediction)
    label = vegetable_classes[np.argmax(prediction)]
    return label, confidence
st.set_page_config(page_title="Vegetable Detector", layout="centered")
st.markdown("<h1 style='text-align: center; color: #90be6d;'>🥗 Vegetable Detector</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #545454;'>Upload a vegetable image or try a sample for detection</h5>", unsafe_allow_html=True)
st.markdown("### 📤 <span style='color:#388e3c'>Upload Your Image</span>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload JPG, JPEG or PNG", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    resized = image.resize((224, 224))
    st.image(resized, caption="Uploaded Image", use_container_width=False)
    label, conf = predict_vegetable(image)
    if conf < 0.4:
        st.error("❌ Not a known vegetable")
    else:
        st.success(f"✅ Detected Vegetable: **{label.upper()}** — Confidence: `{conf:.2f}`")
st.markdown("### 🖼️ <span style='color:#43aa8b'>Try with Sample Images</span>", unsafe_allow_html=True)
sample_dir = 'VegetableDetector/Vegetablesamples'
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
            label, conf = predict_vegetable(img)
            if conf < 0.4:
                st.error("❌ Not a known vegetable")
            else:
                st.success(f"✅ Detected Vegetable: **{label.upper()}**  — Confidence: `{conf:.2f}`")
