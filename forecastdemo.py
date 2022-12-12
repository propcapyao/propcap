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

col9, col10 = st.columns([2, 2])
with col9:
    st.header("Loan Amount Forecasting:")

    gbpyieldforecast = st.radio("GBP 2 year note yield forecast", ["Follow the trend", "Input Manually"])
    if gbpyieldforecast == "Input Manually":
        gbpyieldforecast0 = st.slider("GBP 2 year note yield (%) next 12 months:", 0, 10, 3, 1)
        gbpyieldforecast = [gbpyieldforecast0, gbpyieldforecast0, gbpyieldforecast0, gbpyieldforecast0, gbpyieldforecast0]
    else:
        gbpyieldforecast = [3.289, 4.639, 5.515, 5.972, 6.588]


    quaterlygrowthrate0 = st.slider("Quarterly growth rate (%):", 0, 35, 20, 1)
    quaterlygrowthrate_orig = 0.21
    quaterlygrowthrate = [1.0 + quaterlygrowthrate_orig] * 8 + [1.0 + quaterlygrowthrate0 / 100] * 5

    capacityforecast = 10000000

    loanforecastfile = "loan_forecast.csv"
    loandata = pd.read_csv(loanforecastfile, header = 0)

    loandata["Capacity"] = loandata["Capacity"].fillna(capacityforecast)
    loandata = loandata.drop(["Capacity"], axis = 1)
    loandata["Mortgage Rate Diff"] = loandata["Mortgage Rate"] - loandata["GBP Yield"]
    loandata = loandata.drop(["Mortgage Rate"], axis = 1)
    loandata["UK Property Transactions"] = loandata["UK Property Transactions"].fillna(0) / 1000

    loandata["GBP Yield"].iloc[-5:] = gbpyieldforecast
    #loandata["GBP Yield"] = loandata["GBP Yield"].fillna(method = "ffill")
    #loandata["GBP Yield"] = loandata["GBP Yield"].fillna(gbpyieldforecast0)

    loandata["Growth Factor"] = quaterlygrowthrate
    loandata["Growth Factor"] = loandata["Growth Factor"].cumprod()

    traindata = loandata.dropna()
    forecastdata = loandata[loandata.isna().any(axis = 1)]

    y_train = traindata["Loan Amount"]
    x_train = traindata.drop(["Quarter", "Loan Amount", "Mortgage Rate Diff", "UK Property Transactions"], axis = 1)

    rf1 = linear_model.Ridge()
    rf1.fit(x_train, y_train)

    x_test = forecastdata.drop(["Quarter", "Loan Amount", "Mortgage Rate Diff", "UK Property Transactions"], axis = 1)
    prediction = rf1.predict(x_test)
    forecastdata["Loan Amount"] = np.maximum(prediction, 5 * [0])

    y_train = traindata["Mortgage Rate Diff"]
    x_train = traindata.drop(["Quarter", "Loan Amount", "Mortgage Rate Diff", "Growth Factor", "UK Property Transactions"], axis = 1)

    rf2 = linear_model.Ridge()
    rf2.fit(x_train, y_train)

    x_test = forecastdata.drop(["Quarter", "Loan Amount", "Mortgage Rate Diff", "Growth Factor", "UK Property Transactions"], axis = 1)
    prediction = rf2.predict(x_test)
    forecastdata["Mortgage Rate Diff"] = np.maximum(prediction, 5 * [2.5])
    print(forecastdata)

    loandata = pd.concat([traindata, forecastdata])
    loandata["Loan Amount"] = loandata["Loan Amount"] / 1000000.0
    loandata["Mortgage Rate"] = loandata["GBP Yield"] + loandata["Mortgage Rate Diff"]
    print(loandata)

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
    ax3 = sns.lineplot(data = loandata[:-4], x = "Quarter", y = "Mortgage Rate", color = "blue", marker = "o")
    ax4 = sns.lineplot(data = loandata[-5:], x = "Quarter", y = "Mortgage Rate", color = "skyblue", marker = "o", linestyle = "--")
    ax1.set_xlabel("Quarterly Data")
    ax1.set_ylabel("GBP 2 Year Note Yield (%)")
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax5 = ax1.twinx()
    ax5 = sns.lineplot(data = loandata[:-5], x = "Quarter", y = "UK Property Transactions", color = "limegreen", marker = "o")
    ax5.set_ylabel("No. of UK Property Transactions (k)")
    ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax5.grid(None)
    st.pyplot(fig1)

with col4:
    fig2 = plt.figure()
    sns.set_style("whitegrid")
    color = ["red", "red", "red", "red", "red", "red", "red", "red", "lightpink", "lightpink", "lightpink", "lightpink", "lightpink"]
    ax1 = sns.barplot(data = loandata, x = "Quarter", y = "Loan Amount", palette = color)
    ax1.set_xlabel("Quarterly Data")
    ax1.set_ylabel("Loan Amount (m HKD)")
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))

    st.pyplot(fig2)
