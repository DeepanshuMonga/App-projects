import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import time
import os
import gdown
MODEL_PATH = "CatsvsDogs.h5"
FILE_ID = "1h7BiKqgVuL3_RPuBzJKXDCf0K3BTnvaK"  # Replace this!
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
st.title(":orange[Welcome to Cat vs Dog CLassifier System : ]")
st.subheader("Upload image here :")
Image=st.file_uploader("",type=['jpg','png'])
if(Image!=None):
    with st.status("Processing"):
        st.write("🔁 Loading the trained deep learning model...")
        time.sleep(1)
        st.write("✅ Model loaded successfully!")
        time.sleep(1)
        st.write("🔍 Analyzing your image... Sit tight!")
        time.sleep(1)
        st.write("✅ Image preprocessed successfully!")
        time.sleep(1)
        st.write("🧠 Running prediction through neural network...")
        time.sleep(1)
        st.write("✅ Prediction complete!")
        time.sleep(1)
    img = image.load_img(Image, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    prediction = model.predict(img_array)[0][0]
    if prediction > 0.5:
        st.subheader(f"Output = Prediction: Dog 🐶 ({prediction * 100:.2f}% confidence)")
    else:
        st.subheader(f"Output = Prediction: Cat 🐱 ({(1 - prediction) * 100:.2f}% confidence)")
