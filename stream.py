# Standard Packages:
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

load_time = 0.001

st.set_page_config(page_title="Pauls Pick-Up Line ML", page_icon = '🤖')
st.write("""
# Pauls Pickup Line Machine Learning Project
Icons made by Freepik from www.flaticon.com

## Type your pickup line into the box below.
""")


input_option = st.selectbox("How would you like to deliver your pickup line?",
                            ["Audio", "Text"]
                            )



import time
import data

if input_option == "Text":
    with st.form(key = "my form", clear_on_submit=True):
        input = st.text_input("Enter Your Pickup Line")
        submit_button = st.form_submit_button("Predict")

    if submit_button:
        time.sleep(1)
        predict_function = lambda x: data.predict_a_new_line(x)
        prediction = predict_function(input)

        my_bar = st.progress(0)

        for percent_complete in range(100):
             time.sleep(load_time)
             my_bar.progress(percent_complete + 1)
        time.sleep(1)
        if predict_function(input) == "success":
            st.write("Your pickup line was a " + prediction)
            image = Image.open("heart.png")
            st.image(image, width=150)
        else:
            st.write("Your pickup line was a " + prediction)
            image = Image.open("broken-heart.png")
            st.image(image,width=150)
        my_bar.empty()


if input_option == "Audio":
    st.write("""
    ## Click record, and say your pickup line outloud.

    """)


    import streamlit as st
    from bokeh.models.widgets import Button
    from bokeh.models import CustomJS
    from streamlit_bokeh_events import streamlit_bokeh_events



    stt_button = Button(label="Speak", width=100)

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.continuous = false,
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)



    if result:
        input = result.get("GET_TEXT")
        time.sleep(1)
        if "GET_TEXT" in result:
            st.write(input)
        predict_function = lambda x: data.predict_a_new_line(x)
        prediction = predict_function(input)

        my_bar = st.progress(0)

        for percent_complete in range(100):
             time.sleep(load_time)
             my_bar.progress(percent_complete + 1)
        time.sleep(1)

        if predict_function(input) == "success":
            st.write("Your pickup line was a " + prediction)
            image = Image.open("heart.png")
            st.image(image, width=150)
        else:
            st.write("Your pickup line was a " + prediction)
            image = Image.open("broken-heart.png")
            st.image(image,width=150)
        my_bar.empty()
