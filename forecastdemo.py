import streamlit as st
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn import linear_model

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout = "wide")

def check_password():
    """Returns `True` if the user had a correct password."""
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
    col9, col10 = st.columns([2, 2])
    with col9:
        st.header("Loan Amount Forecasting:")

        gbpyieldforecast = st.radio("GBP 2 year note yield forecast", ["Follow the trend", "Input Manually"])
        if gbpyieldforecast == "Input Manually":
            gbpyieldforecast0  = st.number_input("GBP 2 year note yield (%) next 12 months:", value = 0.0, format = "%f")
            gbpyieldforecast = [gbpyieldforecast0, gbpyieldforecast0, gbpyieldforecast0, gbpyieldforecast0, gbpyieldforecast0]
        else:
            gbpyieldforecast = [3.289, 4.639, 5.515, 5.972, 6.588]

        quaterlygrowthrate0  = st.number_input("Quarterly growth rate (%):", value = 0.0, format = "%f")
        quaterlygrowthrate = 1.0 + quaterlygrowthrate0 / 100

        capacityforecast = 10000000

        loanforecastfile = "loan_forecast.csv"
        loandata = pd.read_csv(loanforecastfile, header = 0)

        loandata["Capacity"] = loandata["Capacity"].fillna(capacityforecast)
        loandata = loandata.drop(["Capacity"], axis = 1)

        loandata["GBP Yield"].iloc[-5:] = gbpyieldforecast
        #loandata["GBP Yield"] = loandata["GBP Yield"].fillna(method = "ffill")
        #loandata["GBP Yield"] = loandata["GBP Yield"].fillna(gbpyieldforecast0)

        loandata["Growth Factor"] = loandata["Growth Factor"].fillna(quaterlygrowthrate)
        loandata["Growth Factor"] = loandata["Growth Factor"].cumprod()

        print(loandata)

        traindata = loandata.dropna()
        forecastdata = loandata[loandata.isna().any(axis = 1)]

        y_train = traindata["Loan Amount"]
        x_train = traindata.drop(["Quarter", "Loan Amount"], axis = 1)

        #rf = RandomForestRegressor()
        #rf = xgb.XGBRegressor(objective = "reg:squarederror")
        rf = linear_model.Ridge()
        rf.fit(x_train, y_train)

        x_test = forecastdata.drop(["Quarter", "Loan Amount"], axis = 1)
        prediction = rf.predict(x_test)
        forecastdata["Loan Amount"].iloc[-5:] = prediction

        loandata = pd.concat([traindata, forecastdata])
        loandata["Loan Amount"] = loandata["Loan Amount"] / 1000000.0

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Loan Amount from 20Q4 to 22Q3 (8 Quarters):")
        total1 = round(loandata[:-5]["Loan Amount"].sum(),1)
        total1 = "Total: " + str(total1) + " Million HKD"
        average1 = round(loandata[:-5]["Loan Amount"].mean(),1)
        average1 = "Average: " + str(average1) + " Million HKD"
        st.subheader(total1)
        st.subheader(average1)

    with col2:
        st.subheader("Loan Amount forecast from 22Q4 to 23Q4 (5 Quarters):")
        print(loandata[-5:])
        total2 = round(loandata[-5:]["Loan Amount"].sum(),1)
        total2 = "Total: " + str(total2) + " Million HKD"
        average2 = round(loandata[-5:]["Loan Amount"].mean(),1)
        average2 = "Average: " + str(average2) + " Million HKD"
        st.subheader(total2)
        st.subheader(average2)

    col3, col4 = st.columns(2)

    with col3:
        fig1 = plt.figure()
        sns.set_style("whitegrid")
        ax1 = sns.lineplot(data = loandata[:-4], x = "Quarter", y = "GBP Yield", color = "red", marker = "o")
        ax2 = sns.lineplot(data = loandata[-5:], x = "Quarter", y = "GBP Yield", color = "lightpink", marker = "o", linestyle = "--")
        ax1.set_xlabel("Quarterly Data")
        ax1.set_ylabel("GBP 2 Year Note Yield (%)")
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
        st.pyplot(fig1)

    with col4:
        fig2 = plt.figure()
        sns.set_style("whitegrid")
        color = ["red", "red", "red", "red", "red", "red", "red", "red", "lightpink", "lightpink", "lightpink", "lightpink", "lightpink"]
        ax3 = sns.barplot(data = loandata, x = "Quarter", y = "Loan Amount", palette = color)
        ax3.set_xlabel("Quarterly Data")
        ax3.set_ylabel("Loan Amount (m HKD)")
        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
        st.pyplot(fig2)
