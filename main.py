import streamlit as st
import pandas as pd
import json
import numpy as np

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout = "wide")

def check_password():
    """Returns `True` if the user had a correct password."""
    st.image("PropCap_Logo.jpeg", width = 150)
    #st.subheader("Please Login:")

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    #st.image("PropCap_Logo.jpeg", width = 150)

    st.markdown("***")

    st.title("AI Powered Mortgage Term Model [link](https://propcapyao-propcap-mrmdemo-8442xy.streamlit.app/)")
    st.title("Quarterly Loan Amount Forecasting [link](https://propcapyao-propcap-forecastdemo-16cpx5.streamlit.app/)")
    st.title("Japanese Credit Information Disclosure Report [link](https://propcapyao-propcap-creditdemo-ve0yf5.streamlit.app/)")
    st.title("Credit Score Report [link](https://creditscorepy-h4tuweruyl5mrx5qseyzx6.streamlit.app/)")
