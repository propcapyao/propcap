import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout = "wide")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("PropCap_Logo.jpeg", width = 150)
with col2:
    st.header("")
    st.title("Class B investment")

fundvalue = st.number_input("Fund Value: ", value = 100000000, format = "%d")
fee = st.number_input("Fund Fee: ", value = 1000000, format = "%d")
hibro = st.number_input("Hibro: ", value = 0.05, format = "%f")
ajustriskonhibro = st.number_input("Adjusted Risk On Hibro: ", value = 0.005, format = "%f")
excessexpectedreturn = st.number_input("Excess Expected Return: ", value = 0.04, format = "%f")

deploydict = {
    0: {
        1:[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.95],
        2:[0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],
        3:[0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],
        4:[0.95, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5, 0.4],
        5:[0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.0, 0.0, 0.0]
    },
    1: {
        2:[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.95],
        3:[0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],
        4:[0.95, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5, 0.4],
        5:[0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.0, 0.0, 0.0]
    },
    2: {
        3:[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.95],
        4:[0.95, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5, 0.4],
        5:[0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.0, 0.0, 0.0]
    },
    3: {
        4:[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        5:[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    4: {
        5:[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
}

investfundvalue = [fundvalue - fee for _ in range(5)]
cummonthlyreturn = pd.DataFrame(columns=['Year', 'Month', 'Return'])
for outer_key, outer_value in deploydict.items():
    print(f'Outer key: {outer_key}')
    for inner_key, inner_value in outer_value.items():
        print(f'  Inner key: {inner_key}')
        annualreturnvalue = 0
        m = 1
        for number in inner_value:
            monthlyreturnvalue = (investfundvalue[outer_key-1]*(1-number)*(hibro-ajustriskonhibro) + (investfundvalue[outer_key-1]*number*(hibro+excessexpectedreturn))) / 12
            monthlyreturn = monthlyreturnvalue / fundvalue
            annualreturnvalue = annualreturnvalue + monthlyreturnvalue
            print(f'    monthlyreturn: {monthlyreturn}')
            new_row = pd.DataFrame({'Year': [inner_key], 'Month': [m], 'Return': [monthlyreturn]})
            cummonthlyreturn = pd.concat([cummonthlyreturn, new_row], ignore_index=True)
            m = m + 1
        annualreturn = annualreturnvalue / fundvalue
        print(f'    annualreturnvalue: {annualreturnvalue}, annualreturn: {annualreturn}')
        if outer_key > 0:
            investfundvalue[inner_key-1] = investfundvalue[inner_key-1] + annualreturnvalue
        else:
            investfundvalue[inner_key-1] = annualreturnvalue
    print(investfundvalue)
    print(sum(investfundvalue))

cummonthlyreturn['TotalMonths'] = (cummonthlyreturn['Year'] - 1) * 12 + cummonthlyreturn['Month']
cummonthlyreturn = cummonthlyreturn.groupby('TotalMonths').agg({'Return':'sum'}).reset_index()
cummonthlyreturn.sort_values(by=['TotalMonths'], inplace=True)

cummonthlyreturn['CumulativeSum_Return'] = cummonthlyreturn['Return'].cumsum()
cummonthlyreturn = cummonthlyreturn.set_index('TotalMonths')

investfundvalue_ = [fundvalue - fee for _ in range(5)]
cummonthlyreturn_ = pd.DataFrame(columns=['Year', 'Month', 'Return'])
for outer_key, outer_value in deploydict.items():
    print(f'Outer key: {outer_key}')
    for inner_key, inner_value in outer_value.items():
        print(f'  Inner key: {inner_key}')
        annualreturnvalue = 0
        i = investfundvalue_[outer_key-1]
        m = 1
        for number in inner_value:
            monthlyreturnvalue = (i*(1-number)*(hibro-ajustriskonhibro) + (i*number*(hibro+excessexpectedreturn))) / 12
            monthlyreturn = monthlyreturnvalue / fundvalue
            annualreturnvalue = annualreturnvalue + monthlyreturnvalue
            print(f'    monthlyreturn: {monthlyreturn}')
            new_row = pd.DataFrame({'Year': [inner_key], 'Month': [m], 'Return': [monthlyreturn]})
            cummonthlyreturn_ = pd.concat([cummonthlyreturn_, new_row], ignore_index=True)
            i = i + monthlyreturnvalue
            m = m + 1
        if outer_key > 0:
            investfundvalue_[inner_key-1] = investfundvalue_[inner_key-1] + annualreturnvalue
        else:
            investfundvalue_[inner_key-1] = annualreturnvalue
        annualreturn = annualreturnvalue / fundvalue
        print(f'    annualreturnvalue: {annualreturnvalue}, annualreturn: {annualreturn}')
    print(investfundvalue_)
    print(sum(investfundvalue_))

print(cummonthlyreturn_)
cummonthlyreturn_['TotalMonths'] = (cummonthlyreturn_['Year'] - 1) * 12 + cummonthlyreturn_['Month']
cummonthlyreturn_ = cummonthlyreturn_.groupby('TotalMonths').agg({'Return':'sum'}).reset_index()
cummonthlyreturn_.sort_values(by=['TotalMonths'], inplace=True)

cummonthlyreturn_['CumulativeSum_Return'] = cummonthlyreturn_['Return'].cumsum()
cummonthlyreturn_ = cummonthlyreturn_.set_index('TotalMonths')


print(cummonthlyreturn)
print(cummonthlyreturn_)
cummonthlyreturn_.columns = ["MonthlyAdjReturn", "MonthAdhjCumulativeSum_Return"]
cummonthlyreturn__ = pd.concat([cummonthlyreturn, cummonthlyreturn_], axis=1)


fig1 = plt.figure()
sns.set_style("whitegrid")
ax1 = sns.lineplot(data=cummonthlyreturn__, x="TotalMonths", y="CumulativeSum_Return", color="red", marker="o", label="CumulativeSum_Return", markersize=3, linewidth = 0.5)
ax3 = sns.lineplot(data=cummonthlyreturn__, x="TotalMonths", y="MonthAdhjCumulativeSum_Return", color="blue", marker="o", label="MonthAdhjCumulativeSum_Return", markersize=3, linewidth = 0.5)
ax1.set_xlabel("Month")
ax1.set_ylabel("Fund Return")
N = 10
ax1.xaxis.set_major_locator(ticker.MaxNLocator(N))
plt.legend()

st.pyplot(fig1)
