# Standard Packages:
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


st.set_page_config(page_title="Pauls Pick-Up Line ML", page_icon = '🤖')
st.write("""
# Pauls Pickup Line Machine Learning Project
Icons made by Freepik from www.flaticon.com
""")



import time
import data
with st.form(key = "my form", clear_on_submit=True):
    input = st.text_input("Enter Your Pickup Line")
    submit_button = st.form_submit_button("Predict")

if submit_button:
    predict_function = lambda x: data.predict_a_new_line(x)
    prediction = predict_function(input)

    my_bar = st.progress(0)

    for percent_complete in range(100):
         time.sleep(0.001)
         my_bar.progress(percent_complete + 1)

    if predict_function(input) == "success":
        st.write("Your pickup line was a " + prediction)
        image = Image.open("heart.png")
        st.image(image, width=150)
    else:
        st.write("Your pickup line was a " + prediction)
        image = Image.open("broken-heart.png")
        st.image(image,width=150)
