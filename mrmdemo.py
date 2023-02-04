import streamlit as st
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google_currency import convert
st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout = "wide")

otherfixfactorbasedrate = 0.0

col9, col10 = st.columns([1, 3])
with col9:
    st.image("PropCap_Logo.jpeg", width = 150)
with col10:
    st.header("")
    st.header("AI Powered Mortgage Term Model")

tab1, tab2 = st.tabs(["Dashboard", "Settings"])

with tab2:
    st.header("Rate Adjustments")
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Base Rate:")
        standardriskspread = st.number_input("Base Rate", value = 0.055, format = "%f")
        st.subheader("Nationality Adjustment Rate:")
        nationality_hk_adj_rate = st.number_input("Hong Kong", value = 0.0, format = "%f")
        nationality_china_adj_rate = st.number_input("China", value = 0.02, format = "%f")
        nationality_japan_adj_rate = st.number_input("Japan", value = 0.0, format = "%f")
        nationality_others_adj_rate = st.number_input("Other Nationality", value = 0.0, format = "%f")
        st.subheader("Employment Type Adjustment Rate:")
        employment_type_government_adj_rate = st.number_input("Government", value = -0.002, format = "%f")
        employment_type_listed_company_adj_rate = st.number_input("Listed Company", value = -0.001, format = "%f")
        employment_type_non_listed_company_adj_rate = st.number_input("Non-listed Company", value = -0.002, format = "%f")
        employment_type_self_employed_adj_rate = st.number_input("Self-Employed", value = 0.001, format = "%f")
        employment_type_retired_adj_rate = st.number_input("Retired", value = 0.002, format = "%f")
        employment_type_others_adj_rate = st.number_input("Other Type", value = 0.0, format = "%f")
        st.subheader("Company Application Adjustment Rate:")
        company_application_adj_rate = st.number_input("Company Flag", value = 0.002, format = "%f")
        st.subheader("Bank Loan Approval Adjustment Rate:")
        bank_loan_approval_adj_rate = st.number_input("Bank Loan Approval Flag", value = -0.0025, format = "%f")
        st.subheader("Property Location Adjustment Rate:")
        st.write("**Australia**")
        property_location_sydney_adj_rate = st.number_input("Sydney", value = 0.0, format = "%f")
        property_location_melbourne_adj_rate = st.number_input("Melbourne", value = 0.0, format = "%f")
        property_location_brisbane_adj_rate = st.number_input("Brisbane", value = 0.0025, format = "%f")
        property_location_gold_coast_adj_rate = st.number_input("Gold Coast", value = 0.005, format = "%f")
        property_location_australia_others_adj_rate = st.number_input("Other Area of Australia", value = 0.005, format = "%f")
        st.write("**Canada**")
        property_location_vancouver_adj_rate = st.number_input("Vancouver", value = 0.0, format = "%f")
        property_location_toronto_adj_rate = st.number_input("Toronto", value = 0.0, format = "%f")
        property_location_calgary_adj_rate = st.number_input("Calgary", value = 0.005, format = "%f")
        property_location_canada_others_adj_rate = st.number_input("Other Area of Canada", value = 0.005, format = "%f")
        st.write("**China**")
        property_location_shanghai_adj_rate = st.number_input("Shanghai", value = 0.0, format = "%f")
        property_location_china_others_adj_rate = st.number_input("Other Area of China", value = 0.005, format = "%f")
        st.write("**Hong Kong**")
        property_location_hk_adj_rate = st.number_input("HK", value = 0.0, format = "%f")
        st.write("**Japan**")
        property_location_tokyo_adj_rate = st.number_input("Tokyo", value = 0.0, format = "%f")
        property_location_osaka_adj_rate = st.number_input("Osaka", value = 0.0, format = "%f")
        property_location_fukuoka_adj_rate = st.number_input("Fukuoka", value = 0.0025, format = "%f")
        property_location_kyoto_adj_rate = st.number_input("Kyoto", value = 0.0025, format = "%f")
        property_location_japan_others_adj_rate = st.number_input("Other Area of Japan", value = 0.005, format = "%f")
        st.write("**South Korea**")
        property_location_seoul_adj_rate = st.number_input("Seoul", value = 0.0, format = "%f")
        property_location_korea_others_adj_rate = st.number_input("Other Area of Korea", value = 0.005, format = "%f")
        st.write("**Taiwan**")
        property_location_taipei_adj_rate = st.number_input("Taipei", value = 0.0, format = "%f")
        property_location_taiwan_others_adj_rate = st.number_input("Other Area of Taiwan", value = 0.005, format = "%f")
        st.write("**UK**")
        property_location_birmingham_adj_rate = st.number_input("Birmingham", value = 0.0025, format = "%f")
        property_location_manchester_adj_rate = st.number_input("Manchester", value = 0.0025, format = "%f")
        property_location_london_adj_rate = st.number_input("London", value = 0.0, format = "%f")
        property_location_uk_others_adj_rate = st.number_input("Other Area of UK", value = 0.005, format = "%f")
        st.write("**Philippine**")
        property_location_manila_adj_rate = st.number_input("Manila", value = 0.005, format = "%f")
        property_location_philippine_others_adj_rate = st.number_input("Other Area of Philippine", value = 0.005, format = "%f")
        st.write("**Other Countries**")
        property_location_other_countries_adj_rate = st.number_input("Other Countries", value = 0.005, format = "%f")
        st.subheader("Tenant Condition Adjustment Rate:")
        tenant_condition_tenanted_adj_rate = st.number_input("Tenanted", value = -0.0015, format = "%f")
        tenant_condition_vacant_adj_rate = st.number_input("Vacant", value = 0.0, format = "%f")
        st.subheader("Property Condition Adjustment Rate:")
        property_condition_new_adj_rate = st.number_input("New", value = 0.0, format = "%f")
        property_condition_liveable_adj_rate = st.number_input("Liveable", value = 0.01, format = "%f")
        property_condition_require_renovation_adj_rate = st.number_input("Require Renovation", value = 0.003, format = "%f")

    with col6:
        st.subheader("Lending Currency Adjustment Rate:")
        st.write("**GBP**")
        lending_ccy_gbp_2_adj_rate = st.number_input("GBP 2 years", value = 0.0349, format = "%f")
        lending_ccy_gbp_5_adj_rate = st.number_input("GBP 5 years", value = 0.0389, format = "%f")
        st.write("**HKD**")
        lending_ccy_hkd_2_adj_rate = st.number_input("HKD 2 years", value = 0.0396, format = "%f")
        lending_ccy_hkd_5_adj_rate = st.number_input("HKD 5 years", value = 0.0399, format = "%f")
        st.write("**USD**")
        lending_ccy_usd_2_adj_rate = st.number_input("USD 2 years", value = 0.0444, format = "%f")
        lending_ccy_usd_5_adj_rate = st.number_input("USD 5 years", value = 0.042, format = "%f")
        st.write("**AUD**")
        lending_ccy_aud_2_adj_rate = st.number_input("AUD 2 years", value = 0.0337, format = "%f")
        lending_ccy_aud_5_adj_rate = st.number_input("AUD 5 years", value = 0.0367, format = "%f")
        st.write("**JPY**")
        lending_ccy_jpy_2_adj_rate = st.number_input("JPY 2 years", value = -0.0006, format = "%f")
        lending_ccy_jpy_5_adj_rate = st.number_input("JPY 5 years", value = 0.0009, format = "%f")
        st.subheader("Property Type Adjustment Rate:")
        st.write("**UK Flat / Condo**")
        property_type_uk_flat_condo_studio_adj_rate = st.number_input("UK Flat / Condo Studio", value = 0.0025, format = "%f")
        property_type_uk_flat_condo_1_adj_rate = st.number_input("UK Flat / Condo 1 Bedroom", value = 0.0, format = "%f")
        property_type_uk_flat_condo_2_adj_rate = st.number_input("UK Flat / Condo 2 Bedrooms", value = 0.0, format = "%f")
        property_type_uk_flat_condo_3_adj_rate = st.number_input("UK Flat / Condo 3+ Bedrooms", value = 0.001, format = "%f")
        st.write("**Japan Flat / Condo**")
        property_type_japan_flat_condo_studio_adj_rate = st.number_input("Japan Flat / Condo Studio", value = 0.001, format = "%f")
        property_type_japan_flat_condo_1_adj_rate = st.number_input("Japan Flat / Condo 1 Bedroom", value = 0.0, format = "%f")
        property_type_japan_flat_condo_2_adj_rate = st.number_input("Japan Flat / Condo 2 Bedrooms", value = 0.0, format = "%f")
        property_type_japan_flat_condo_3_adj_rate = st.number_input("Japan Flat / Condo 3+ Bedrooms", value = 0.001, format = "%f")
        st.write("**UK Detached**")
        property_type_uk_detached_1_adj_rate = st.number_input("UK Detached 1 Bedroom", value = 0.0, format = "%f")
        property_type_uk_detached_2_adj_rate = st.number_input("UK Detached 2 Bedrooms", value = 0.0, format = "%f")
        property_type_uk_detached_3_adj_rate = st.number_input("UK Detached 3+ Bedrooms", value = 0.0, format = "%f")
        st.write("**Japan Detached**")
        property_type_japan_detached_1_adj_rate = st.number_input("Japan Detached 1 Bedroom", value = 0.003, format = "%f")
        property_type_japan_detached_2_adj_rate = st.number_input("Japan Detached 2 Bedrooms", value = 0.003, format = "%f")
        property_type_japan_detached_3_adj_rate = st.number_input("Japan Detached 3+ Bedrooms", value = 0.003, format = "%f")
        st.write("**UK Semi Detached**")
        property_type_uk_semi_detached_1_adj_rate = st.number_input("UK Semi Detached 1 Bedroom", value = 0.0, format = "%f")
        property_type_uk_semi_detached_2_adj_rate = st.number_input("UK Semi Detached 2 Bedrooms", value = 0.0, format = "%f")
        property_type_uk_semi_detached_3_adj_rate = st.number_input("UK Semi Detached 3+ Bedrooms", value = 0.0, format = "%f")
        st.write("**Japan Semi Detached**")
        property_type_japan_semi_detached_1_adj_rate = st.number_input("Japan Semi Detached 1 Bedroom", value = 0.003, format = "%f")
        property_type_japan_semi_detached_2_adj_rate = st.number_input("Japan Semi Detached 2 Bedrooms", value = 0.003, format = "%f")
        property_type_japan_semi_detached_3_adj_rate = st.number_input("Japan Semi Detached 3+ Bedrooms", value = 0.003, format = "%f")
        st.write("**UK Terraced**")
        property_type_uk_terraced_1_adj_rate = st.number_input("UK Terraced 1 Bedroom", value = 0.0, format = "%f")
        property_type_uk_terraced_2_adj_rate = st.number_input("UK Terraced 2 Bedrooms", value = 0.0, format = "%f")
        property_type_uk_terraced_3_adj_rate = st.number_input("UK Terraced 3+ Bedrooms", value = 0.0, format = "%f")
        st.write("**Japan Terraced**")
        property_type_japan_terraced_1_adj_rate = st.number_input("Japan Terraced 1 Bedroom", value = 0.003, format = "%f")
        property_type_japan_terraced_2_adj_rate = st.number_input("Japan Terraced 2 Bedrooms", value = 0.003, format = "%f")
        property_type_japan_terraced_3_adj_rate = st.number_input("Japan Terraced 3+ Bedrooms", value = 0.003, format = "%f")
        st.write("**HMO**")
        property_type_uk_hmo_adj_rate = st.number_input("UK HMO", value = 0.005, format = "%f")
        property_type_japan_hmo_adj_rate = st.number_input("Japan HMO", value = 0.005, format = "%f")
        st.write("**Bungalow**")
        property_type_uk_bungalow_adj_rate = st.number_input("UK Bungalow", value = 0.005, format = "%f")
        property_type_japan_bungalow_adj_rate = st.number_input("Japan Bungalow", value = 0.005, format = "%f")
        st.write("**Land**")
        property_type_uk_land_adj_rate = st.number_input("UK Land", value = 0.005, format = "%f")
        property_type_japan_land_adj_rate = st.number_input("Japan Land", value = 0.005, format = "%f")
        st.write("**Commercial**")
        property_type_uk_commercial_adj_rate = st.number_input("UK Commercial", value = 0.005, format = "%f")
        property_type_japan_commercial_adj_rate = st.number_input("Japan Commercial", value = 0.005, format = "%f")
        st.subheader("ESG Flag Adjustment Rate:")
        esg_adj_rate = st.number_input("ESG Flag", value = -0.001, format = "%f")

    st.markdown("***")
    st.header("Risk Coefficents")
    col7, col8 = st.columns(2)

    with col7:
        st.subheader("Yearly Income Coefficents")
        wage_coefficent = st.number_input("Wages", value = 0.9, format = "%f")
        interest_dividend_coefficent = st.number_input("Interest / Dividends", value = 0.8, format = "%f")
        partner_income_coefficent = st.number_input("Spouse / Partner Income", value = 0.9, format = "%f")
        rental_income_coefficent = st.number_input("Rental Income", value = 0.8, format = "%f")
        investment_income_coefficent = st.number_input("Investment Income", value = 0.7, format = "%f")
        other_income_coefficent = st.number_input("Other Income", value = 0.6, format = "%f")
        st.subheader("Yearly Regular Expenditures Coefficents")
        wage_coefficent = st.number_input("Residential / Investment Mortgage", value = 1.0, format = "%f")
        annuity_rent_coefficent = st.number_input("Annuity / Rent", value = 1.0, format = "%f")
        loan_expense_coefficent = st.number_input("Personal Finance Loans / Installment Purchases", value = 1.1, format = "%f")
        household_expense_coefficent = st.number_input("Household Expenses", value = 1.0, format = "%f")
        other_expense_coefficent = st.number_input("Other Expense", value = 1.0, format = "%f")
    with col8:
        st.subheader("Real Estate Asset and Liabilities Coefficents")
        deposits_coefficent = st.number_input("Deposits", value = 1.0, format = "%f")
        bonds_coefficent = st.number_input("Bonds", value = 0.9, format = "%f")
        pensions_coefficent = st.number_input("Pensions", value = 0.6, format = "%f")
        stocks_fund_income_coefficent = st.number_input("Stocks /Fund", value = 0.75, format = "%f")
        other_assets_income_coefficent = st.number_input("Other Assets", value = 0.6, format = "%f")
        real_assets_income_coefficent = st.number_input("Real Estates", value = 0.3, format = "%f")
        personal_loans_coefficent = st.number_input("Personal Loans", value = 1.0, format = "%f")
        car_loans_coefficent = st.number_input("Car Loans", value = 1.0, format = "%f")
        tax_loans_coefficent = st.number_input("Tax Loans", value = 1.0, format = "%f")
        other_loans_coefficent = st.number_input("Other Loans", value = 1.0, format = "%f")
        mortgage_loans_coefficent = st.number_input("Mortgage", value = 1.0, format = "%f")


st.sidebar.header("Borrower Personal Details:")
nationality = st.sidebar.selectbox("Nationality", ["Hong Kong", "China", "Japan", "Others"])
if nationality == "Hong Kong":
    otherfixfactorbasedrate += nationality_hk_adj_rate
elif nationality == "China":
    otherfixfactorbasedrate += nationality_china_adj_rate
elif nationality == "Japan":
    otherfixfactorbasedrate += nationality_japan_adj_rate
elif nationality == "Others":
    otherfixfactorbasedrate += nationality_others_adj_rate

employment_type = st.sidebar.selectbox("Employment Type", ["Government", "Listed Company", "Non-listed Company", "Self-Employed", "Retired", "Others"])
if employment_type == "Government":
    otherfixfactorbasedrate += employment_type_government_adj_rate
elif employment_type == "Listed Company":
    otherfixfactorbasedrate += employment_type_listed_company_adj_rate
elif employment_type == "Non-listed Company":
    otherfixfactorbasedrate += employment_type_non_listed_company_adj_rate
elif employment_type == "Self-Employed":
    otherfixfactorbasedrate += employment_type_self_employed_adj_rate
elif employment_type == "Retired":
    otherfixfactorbasedrate += employment_type_retired_adj_rate
elif employment_type == "Others":
    otherfixfactorbasedrate += employment_type_others_adj_rate

company_flag = st.sidebar.checkbox("Company Application")
if company_flag:
    otherfixfactorbasedrate += company_application_adj_rate

st.sidebar.header("Personal Income and Expenditures (HKD):")
st.sidebar.subheader("Yearly Income")

wage = st.sidebar.number_input("Wages", value = 1000000, format = "%d") * wage_coefficent
interest_dividend = st.sidebar.number_input("Interest / Dividends", value = 100000, format = "%d") * interest_dividend_coefficent
partner_income = st.sidebar.number_input("Spouse / Partner Income", value = 500000, format = "%d") * partner_income_coefficent
rental_income = st.sidebar.number_input("Rental Income", value = 100000, format = "%d") * rental_income_coefficent
investment_income = st.sidebar.number_input("Investment Income", value = 1000000, format = "%d") * investment_income_coefficent
other_income = st.sidebar.number_input("Other Income", value = 100000, format = "%d") * other_income_coefficent

totalannualincome = wage + interest_dividend + partner_income + rental_income + investment_income + other_income

st.sidebar.subheader("Yearly Regular Expenditures")

mortgage_expense = st.sidebar.number_input("Residential / Investment Mortgage", value = 500000, format = "%d") * wage_coefficent
annuity_rent_expense = st.sidebar.number_input("Annuity / Rent", value = 500000, format = "%d") * annuity_rent_coefficent
loan_expense = st.sidebar.number_input("Personal Finance Loans / Installment Purchases", value = 100000, format = "%d") * loan_expense_coefficent
household_expense = st.sidebar.number_input("Household Expenses", value = 500000, format = "%d") * household_expense_coefficent
other_expense = st.sidebar.number_input("Other Expense", value = 100000, format = "%d") * other_expense_coefficent

totalannualcommitments = mortgage_expense + annuity_rent_expense + loan_expense + household_expense + other_expense

st.sidebar.header("Asset and Liabilities (HKD):")

st.sidebar.subheader("Assets")

deposits = st.sidebar.number_input("Deposits", value = 1000000, format = "%d") * deposits_coefficent
bonds = st.sidebar.number_input("Bonds", value = 100000, format = "%d") * bonds_coefficent
pensions = st.sidebar.number_input("Pensions", value = 1000000, format = "%d") * pensions_coefficent
stocks_funds = st.sidebar.number_input("Stocks /Fund", value = 500000, format = "%d") * stocks_fund_income_coefficent
other_assets = st.sidebar.number_input("Other Assets", value = 500000, format = "%d") * other_assets_income_coefficent
real_estates = st.sidebar.number_input("Real Estates", value = 5000000, format = "%d") * real_assets_income_coefficent
nonpropertyassets = deposits + bonds + pensions + stocks_funds + other_assets
propertyassets = real_estates

st.sidebar.subheader("Liabilities")

personal_loans = st.sidebar.number_input("Personal Loans", value = 1000000, format = "%d") * personal_loans_coefficent
car_loans = st.sidebar.number_input("Car Loans", value = 100000, format = "%d") * car_loans_coefficent
tax_loans = st.sidebar.number_input("Tax Loans", value = 100000, format = "%d") * tax_loans_coefficent
other_loans = st.sidebar.number_input("Other Loans", value = 100000, format = "%d") * other_loans_coefficent
mortgage_loans = st.sidebar.number_input("Mortgage", value = 5000000, format = "%d") * mortgage_loans_coefficent
totalliabilities = personal_loans + car_loans + tax_loans + other_loans + mortgage_loans

st.sidebar.header("Other Factors:")
bankloanapproval_flag = st.sidebar.checkbox("Bank Loan Approval")
if bankloanapproval_flag:
    otherfixfactorbasedrate += bank_loan_approval_adj_rate
secondmortgage_flag = st.sidebar.checkbox("Second Mortgage")

st.sidebar.markdown("***")

with tab1:
    st.subheader("Security Details:")
    col1, col2 = st.columns(2)
    with col1:
        security_value_ccy = st.selectbox("Security Value Currency", ["GBP", "HKD", "USD", "AUD", "JPY"])
        security_value = st.number_input("Security Value (" + security_value_ccy + ")", value = 1000000, format = "%d")

        propertyvalue = float(json.loads(convert(security_value_ccy, "HKD", security_value))["amount"])

        proposed_annual_rent = st.number_input("Proposed Annual Rent (HKD)", value = 500000, format = "%d")
        proposedannualrent = proposed_annual_rent

        property_country = st.selectbox("Property Country", ["Australia", "Canada", "China", "Hong Kong", "Japan", "South Korea", "Taiwan", "UK", "Philippine", "Others"])
        if property_country == "Australia":
            property_location = st.selectbox("Property location", ["Sydney", "Melbourne", "Brisbane", "Gold Coast", "Others"])
            if property_location == "Sydney":
                otherfixfactorbasedrate += property_location_sydney_adj_rate
            elif property_location == "Melbourne":
                otherfixfactorbasedrate += property_location_melbourne_adj_rate
            elif property_location == "Brisbane":
                otherfixfactorbasedrate += property_location_brisbane_adj_rate
            elif property_location == "Gold Coast":
                otherfixfactorbasedrate += property_location_gold_coast_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_australia_others_adj_rate
        elif property_country == "Canada":
            property_location = st.selectbox("Property location", ["Vancouver", "Toronto", "Calgary", "Others"])
            if property_location == "Vancouver":
                otherfixfactorbasedrate += property_location_vancouver_adj_rate
            elif property_location == "Toronto":
                otherfixfactorbasedrate += property_location_toronto_adj_rate
            elif property_location == "Calgary":
                otherfixfactorbasedrate += property_location_calgary_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_canada_others_adj_rate
        elif property_country == "China":
            property_location = st.selectbox("Property location", ["Shanghai", "Others"])
            if property_location == "Shanghai":
                otherfixfactorbasedrate += property_location_shanghai_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_china_others_adj_rate
        elif property_country == "Hong Kong":
            property_location = st.selectbox("Property location", ["Hong Kong"])
            otherfixfactorbasedrate += property_location_hk_adj_rate
        elif property_country == "Japan":
            property_location = st.selectbox("Property location", ["Tokyo", "Osaka", "Fukuoka", "Kyoto", "Others"])
            if property_location == "Tokyo":
                otherfixfactorbasedrate += property_location_tokyo_adj_rate
            elif property_location == "Osaka":
                otherfixfactorbasedrate += property_location_osaka_adj_rate
            elif property_location == "Fukuoka":
                otherfixfactorbasedrate += property_location_fukuoka_adj_rate
            elif property_location == "Kyoto":
                otherfixfactorbasedrate += property_location_kyoto_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_japan_others_adj_rate
        elif property_country == "South Korea":
            property_location = st.selectbox("Property location", ["Seoul", "Others"])
            if property_location == "Seoul":
                otherfixfactorbasedrate += property_location_seoul_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_korea_others_adj_rate
        elif property_country == "Taiwan":
            property_location = st.selectbox("Property location", ["Taipei", "Others"])
            if property_location == "Taipei":
                otherfixfactorbasedrate += property_location_taipei_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_taiwan_others_adj_rate
        elif property_country == "UK":
            property_location = st.selectbox("Property location", ["Birmingham", "Manchester", "London", "Others"])
            if property_location == "Birmingham":
                otherfixfactorbasedrate += property_location_birmingham_adj_rate
            elif property_location == "Manchester":
                otherfixfactorbasedrate += property_location_manchester_adj_rate
            elif property_location == "London":
                otherfixfactorbasedrate += property_location_london_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_uk_others_adj_rate
        elif property_country == "Philippine":
            property_location = st.selectbox("Property location", ["Manila", "Others"])
            if property_location == "Manila":
                otherfixfactorbasedrate += property_location_manila_adj_rate
            elif property_location == "Others":
                otherfixfactorbasedrate += property_location_philippine_others_adj_rate
        else:
            property_location = st.selectbox("Property location", ["Others"])
            otherfixfactorbasedrate += property_location_other_countries_adj_rate

        lending_ccy = st.selectbox("Lending Currency", ["GBP", "HKD", "USD", "AUD", "JPY"])

    with col2:
        loan_term = st.slider("Loan Term (months)", 0, 60, 24, 6)
        if loan_term <= 24:
            lending_yield_curve = 2
        else:
            lending_yield_curve = 5
        if lending_ccy == "GBP":
            if lending_yield_curve == 2:
                lendingccybasedrate = lending_ccy_gbp_2_adj_rate
            elif lending_yield_curve == 5:
                lendingccybasedrate = lending_ccy_gbp_5_adj_rate
        elif lending_ccy == "HKD":
            if lending_yield_curve == 2:
                lendingccybasedrate = lending_ccy_hkd_2_adj_rate
            elif lending_yield_curve == 5:
                lendingccybasedrate = lending_ccy_hkd_5_adj_rate
        elif lending_ccy == "USD":
            if lending_yield_curve == 2:
                lendingccybasedrate = lending_ccy_usd_2_adj_rate
            elif lending_yield_curve == 5:
                lendingccybasedrate = lending_ccy_usd_5_adj_rate
        elif lending_ccy == "AUD":
            if lending_yield_curve == 2:
                lendingccybasedrate = lending_ccy_aud_2_adj_rate
            elif lending_yield_curve == 5:
                lendingccybasedrate = lending_ccy_aud_5_adj_rate
        elif lending_ccy == "JPY":
            if lending_yield_curve == 2:
                lendingccybasedrate = lending_ccy_jpy_2_adj_rate
            elif lending_yield_curve == 5:
                lendingccybasedrate = lending_ccy_jpy_5_adj_rate

        tenant_condition = st.radio("Tenant Condition", options = ["Tenanted", "Vacant"])
        if tenant_condition == "Tenanted":
            otherfixfactorbasedrate += tenant_condition_tenanted_adj_rate
        elif tenant_condition == "Vacant":
            otherfixfactorbasedrate += tenant_condition_vacant_adj_rate

        property_type = st.selectbox("Property Type", ["Flat / Condo", "Detached", "Semi Detached", "Terraced", "HMO", "Bungalow", "Land", "Commercial"])
        if property_type == "Flat / Condo":
            bedrooms = st.selectbox("No. of Bedrooms", ["Studio", "1 Bedroom", "2 Bedrooms", "3+ Bedrooms"])
            if property_country == "UK":
                if bedrooms == "Studio":
                    otherfixfactorbasedrate += property_type_uk_flat_condo_studio_adj_rate
                elif bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_flat_condo_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_flat_condo_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_uk_flat_condo_3_adj_rate
            elif property_country == "Japan":
                if bedrooms == "Studio":
                    otherfixfactorbasedrate += property_type_japan_flat_condo_studio_adj_rate
                elif bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_flat_condo_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_flat_condo_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_japan_flat_condo_3_adj_rate
        elif property_type == "Detached":
            bedrooms = st.selectbox("No. of Bedrooms", ["1 Bedroom", "2 Bedrooms", "3+ Bedrooms"])
            if property_country == "UK":
                if bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_detached_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_detached_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_uk_detached_3_adj_rate
            elif property_country == "Japan":
                if bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_detached_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_detached_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_japan_detached_3_adj_rate
        elif property_type == "Semi Detached":
            bedrooms = st.selectbox("No. of Bedrooms", ["1 Bedroom", "2 Bedrooms", "3+ Bedrooms"])
            if property_country == "UK":
                if bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_semi_detached_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_semi_detached_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_uk_semi_detached_3_adj_rate
            elif property_country == "Japan":
                if bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_semi_detached_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_semi_detached_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_japan_semi_detached_3_adj_rate
        elif property_type == "Terraced":
            bedrooms = st.selectbox("No. of Bedrooms", ["1 Bedroom", "2 Bedrooms", "3+ Bedrooms"])
            if property_country == "UK":
                if bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_terraced_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_uk_terraced_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_uk_terraced_3_adj_rate
            elif property_country == "Japan":
                if bedrooms == "1 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_terraced_1_adj_rate
                elif bedrooms == "2 Bedroom":
                    otherfixfactorbasedrate += property_type_japan_terraced_2_adj_rate
                elif bedrooms == "3+ Bedroom":
                    otherfixfactorbasedrate += property_type_japan_terraced_3_adj_rate
        elif property_type == "HMO":
            bedrooms = st.selectbox("No. of Bedrooms", ["None"])
            if property_country == "UK":
                otherfixfactorbasedrate += property_type_uk_hmo_adj_rate
            elif property_country == "Japan":
                otherfixfactorbasedrate += property_type_japan_hmo_adj_rate
        elif property_type == "Bungalow":
            bedrooms = st.selectbox("No. of Bedrooms", ["None"])
            if property_country == "UK":
                otherfixfactorbasedrate += property_type_uk_bungalow_adj_rate
            elif property_country == "Japan":
                otherfixfactorbasedrate += property_type_japan_bungalow_adj_rate
        elif property_type == "Land":
            bedrooms = st.selectbox("No. of Bedrooms", ["None"])
            if property_country == "UK":
                otherfixfactorbasedrate += property_type_uk_land_adj_rate
            elif property_country == "Japan":
                otherfixfactorbasedrate += property_type_japan_land_adj_rate
        elif property_type == "Commercial":
            bedrooms = st.selectbox("No. of Bedrooms", ["None"])
            if property_country == "UK":
                otherfixfactorbasedrate += property_type_uk_commercial_adj_rate
            elif property_country == "Japan":
                otherfixfactorbasedrate += property_type_japan_commercial_adj_rate

        property_condition = st.radio("Property Condition", options = ["New", "Liveable", "Require Renovation"])
        if property_condition == "New":
            otherfixfactorbasedrate += property_condition_new_adj_rate
        elif property_condition == "Liveable":
            otherfixfactorbasedrate += property_condition_liveable_adj_rate
        elif property_condition == "Require Renovation":
            otherfixfactorbasedrate += property_condition_require_renovation_adj_rate
        esg_flag = st.checkbox("ESG Compliance", value = True)
        if esg_flag:
            otherfixfactorbasedrate += esg_adj_rate

    resultpairs = pd.DataFrame(columns = ["InterestRate", "LVR"])

    totalassets = propertyassets + nonpropertyassets
    networth = totalassets - totalliabilities
    financialassets = nonpropertyassets - totalliabilities

    for lvr in np.arange(0.35, 0.86, 0.01):
        for interestrate in np.arange(0.05, 0.25, 0.0001):
            lvr = float("{0:.2f}".format(lvr))
            interestrate = float("{0:.4f}".format(interestrate))
            totalinterestpayment = propertyvalue * lvr * interestrate
            proposedloanamount = propertyvalue * lvr

            titeratio = (totalannualincome + proposedannualrent) / (totalannualcommitments + totalinterestpayment)
            nalaratio = proposedloanamount / networth
            na24iratio = networth / totalinterestpayment
            fa24iratio = financialassets / totalinterestpayment

            if titeratio > 3:
                titescore = 5
            elif titeratio > 2:
                titescore = 4
            elif titeratio > 1.5:
                titescore = 3
            elif titeratio > 1.25:
                titescore = 2
            elif titeratio > 1:
                titescore = 1
            else:
                titescore = 0

            if nalaratio > 1:
                nalascore = 5
            elif nalaratio > 0.75:
                nalascore = 4
            elif nalaratio > 0.5:
                nalascore = 3
            elif nalaratio > 0.25:
                nalascore = 2
            elif nalaratio > 0:
                nalascore = 1
            else:
                nalascore = 0

            if na24iratio > 25:
                na24iscore = 5
            elif na24iratio > 15:
                na24iscore = 4
            elif na24iratio > 10:
                na24iscore = 3
            elif na24iratio > 5:
                na24iscore = 2
            elif na24iratio > 2:
                na24iscore = 1
            else:
                na24iscore = 0

            if fa24iratio > 10:
                fa24iscore = 5
            elif fa24iratio > 5:
                fa24iscore = 4
            elif fa24iratio > 2:
                fa24iscore = 3
            elif fa24iratio > 1:
                fa24iscore = 2
            elif fa24iratio > 0:
                fa24iscore = 1
            else:
                fa24iscore = 0

            financialscore = (titescore + nalascore + na24iscore + fa24iscore) / 4.0

            if financialscore > 4:
                financialscorebasedrate = -0.0025
            elif financialscore > 3:
                financialscorebasedrate = -0.0
            elif financialscore > 2:
                financialscorebasedrate = 0.0025
            elif financialscore > 1:
                financialscorebasedrate = 0.005
            else:
                financialscorebasedrate = 0.0075

            if proposedloanamount < 1200000:
                proposedloanbasedrate = 0.0
            elif proposedloanamount < 2000000:
                proposedloanbasedrate = 0.003
            elif proposedloanamount < 3000000:
                proposedloanbasedrate = 0.005
            elif proposedloanamount < 4000000:
                proposedloanbasedrate = 0.008
            else:
                proposedloanbasedrate = 0.012

            if lvr < 0.4:
                lvrbasedrate = -0.0025
            elif lvr < 0.5:
                lvrbasedrate = -0.0015
            elif lvr < 0.6:
                lvrbasedrate = -0.001
            elif lvr < 0.65:
                lvrbasedrate = 0.0
            elif lvr < 0.7:
                lvrbasedrate = 0.0025
            elif lvr < 0.75:
                lvrbasedrate = 0.006
            else:
                lvrbasedrate = 0.01

            secondmortgagebasedrate = 0.0

            if secondmortgage_flag:
                if lvr < 0.65:
                    secondmortgagebasedrate = 0.05
                if lvr < 0.75:
                    secondmortgagebasedrate = 0.06
                else:
                    secondmortgagebasedrate = 0.08

            testrate_rounded = float("{0:.4f}".format(standardriskspread + lendingccybasedrate + otherfixfactorbasedrate + financialscorebasedrate + proposedloanbasedrate + lvrbasedrate + secondmortgagebasedrate))
            if testrate_rounded == interestrate:
                resultpairs.loc[len(resultpairs)] = [float("{0:.4f}".format(interestrate)), lvr]

    st.markdown("***")

    st.subheader("Mortgage Rate by LVR:")
    col3, col4 = st.columns([3, 1])

    with col3:
        if len(resultpairs) == 0:
            print("No valid result.")
        else:
            resultpairs_ = resultpairs * 100
            resultpairs_ = (resultpairs_[(resultpairs_["LVR"] / 5.0).astype(int) == (resultpairs_["LVR"] / 5.0)]).reset_index(drop = True)
            fig = plt.figure()
            sns.set_style("whitegrid")
            ax = sns.lineplot(data = resultpairs_, x = "LVR", y = "InterestRate", color = "red", marker = "o")
            ax.set_xlabel("Loan to Value (%)")
            ax.set_ylabel("Interest Rate (%)")
            st.pyplot(fig)
    with col4:
        resultpairs_.columns = ["InterestRate (%)", "LVR (%)"]
        st.table(resultpairs_[["LVR (%)", "InterestRate (%)"]].style.format({"LVR (%)": "{:.0f}", "InterestRate (%)": "{:.1f}"}))

    st.markdown("***")
    col11, col12 = st.columns([1, 1])

    with col11:
        lvr2 = st.number_input("LVR (%):", value = 35, format = "%d")
        lvr2 = lvr2 / 100
        interestrate2 = st.number_input("Interest Rate (%):", value = 8, format = "%d")
        interestrate2 = interestrate2 / 100
        st.subheader("Total Assets (HKD):")
        st.text(totalassets)
        st.subheader("Total Liabilities (HKD):")
        st.text(totalliabilities)
        st.subheader("Net Worth (HKD):")
        st.text(networth)

        st.subheader("Purchase Price (HKD):")
        st.text(round(propertyvalue,1))
        st.subheader("Loan Amount (HKD):")
        proposedloanamount2 = propertyvalue * lvr2
        st.text(round(proposedloanamount2,1))

    with col12:
        st.subheader("Asset Coverage Ratio:")
        st.text(round(networth/proposedloanamount2,2))
        st.subheader("Annual Rental Income (HKD):")
        st.text(proposedannualrent)
        st.subheader("Annual Interest Payment (HKD):")
        totalinterestpayment2 = proposedloanamount2 * interestrate2
        st.text(round(totalinterestpayment2,1))
        st.subheader("Interest Coverage Ratio:")
        st.text(round(proposedannualrent/totalinterestpayment2,2))

        st.subheader("Total Annual Commitments (HKD):")
        totalannualcommitments2 = totalannualcommitments + totalinterestpayment2
        st.text(round(totalannualcommitments2,1))
        st.subheader("Total Income (HKD):")
        totalannualincome2 = totalannualincome + proposedannualrent
        st.text(round(totalannualincome2,1))
        st.subheader("Debt Servicing Ratio:")
        st.text(round(totalannualcommitments2/totalannualincome2,2))

