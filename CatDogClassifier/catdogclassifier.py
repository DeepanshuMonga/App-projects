import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import time
st.title(":orange[Welcome to Cat vs Dog CLassifier System : ]")
model = load_model(r"C:\Users\monga\OneDrive\Desktop\Coding\CatsvsDogs.h5")
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