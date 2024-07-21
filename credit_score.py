import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, mannwhitneyu, entropy, gaussian_kde

# Function to compute CDF
def compute_cdf(data):
    sorted_data = np.sort(data)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    return sorted_data, cdf

# Helper functions for statistical computations
def jensen_shannon_divergence(p, q):
    m = 0.5 * (p + q)
    return 0.5 * (entropy(p, m) + entropy(q, m))

def hellinger_distance(p, q):
    return np.linalg.norm(np.sqrt(p) - np.sqrt(q)) / np.sqrt(2)

# Start building Streamlit app
st.title('Credit Data Analysis')

# Financial Data Inputs
st.sidebar.title("Financial Inputs")
totalinterestpayment = st.sidebar.number_input("Total Interest Payment", min_value=0.0, value=100000.0, format="%.2f")  # Default value set to 1000.0
proposedloanamount = st.sidebar.number_input("Proposed Loan Amount", min_value=0.0, value=500000.0, format="%.2f")  # Default value set to 50000.0
propertyassets = st.sidebar.number_input("Property Assets", min_value=0.0, value=10000000.0, format="%.2f")  # Default value set to 200000.0
nonpropertyassets = st.sidebar.number_input("Non-Property Assets", min_value=0.0, value=1000000.0, format="%.2f")  # Default value set to 50000.0
totalliabilities = st.sidebar.number_input("Total Liabilities", min_value=0.0, value=5000000.0, format="%.2f")  # Default value set to 100000.0
totalannualincome = st.sidebar.number_input("Total Annual Income", min_value=0.0, value=500000.0, format="%.2f")  # Default value set to 75000.0
proposedannualrent = st.sidebar.number_input("Proposed Annual Rent", min_value=0.0, value=150000.0, format="%.2f")  # Default value set to 12000.0
totalannualcommitments = st.sidebar.number_input("Total Annual Commitments", min_value=0.0, value=400000.0, format="%.2f")  # Default value set to 15000.0

# Upload the CSV files
st.sidebar.title("Upload Files")
#uploaded_file_mortgage = st.sidebar.file_uploader("Choose a file for bank statement with mortgage", type=['csv'])
#uploaded_file_without_mortgage = st.sidebar.file_uploader("Choose a file for bank statement without mortgage", type=['csv'])

uploaded_file_mortgage = "bank_statement_with_mortgage.csv"
uploaded_file_without_mortgage = "bank_statement.csv"

if uploaded_file_mortgage and uploaded_file_without_mortgage:
    bank_with_mortgage_df = pd.read_csv(uploaded_file_mortgage)
    bank_df = pd.read_csv(uploaded_file_without_mortgage)

    # Compute the CDFs
    bank_with_mortgage_sorted, cdf_with_mortgage = compute_cdf(bank_with_mortgage_df['Amount'])
    bank_sorted, cdf_bank = compute_cdf(bank_df['Amount'])

    # Interpolate the CDFs to have matching x-values
    common_amounts = np.union1d(bank_with_mortgage_sorted, bank_sorted)
    interpolated_cdf_with_mortgage = np.interp(common_amounts, bank_with_mortgage_sorted, cdf_with_mortgage)
    interpolated_cdf_bank = np.interp(common_amounts, bank_sorted, cdf_bank)

    # K-S Test Plot
    D, p_value_ks = ks_2samp(bank_with_mortgage_df['Amount'], bank_df['Amount'])
    inverted_score_ks = 1 - D
    fig_ks, ax_ks = plt.subplots()
    ax_ks.plot(bank_with_mortgage_sorted, cdf_with_mortgage, label='With Mortgage', color='blue')
    ax_ks.plot(bank_sorted, cdf_bank, label='Without Mortgage', color='red', linestyle='--')
    ax_ks.set_title('K-S Test CDFs')
    ax_ks.legend()

    # Mann-Whitney U Test Plot
    u_statistic, p_value_mw = mannwhitneyu(bank_with_mortgage_df['Amount'], bank_df['Amount'], alternative='two-sided')
    score_mwu = 1 - (u_statistic / (len(bank_with_mortgage_df['Amount']) * len(bank_df['Amount'])))
    fig_mw, ax_mw = plt.subplots()
    ax_mw.plot(common_amounts, interpolated_cdf_with_mortgage, label='With Mortgage', color='blue')
    ax_mw.plot(common_amounts, interpolated_cdf_bank, label='Without Mortgage', color='red', linestyle='--')
    ax_mw.set_title('Mann-Whitney U Test CDFs')
    ax_mw.legend()

    # JSD Plot
    jsd_cdf = jensen_shannon_divergence(interpolated_cdf_with_mortgage, interpolated_cdf_bank)
    score_jsd_cdf = 1 - np.sqrt(jsd_cdf)
    fig_jsd, ax_jsd = plt.subplots()
    ax_jsd.plot(common_amounts, interpolated_cdf_with_mortgage, label='With Mortgage', color='blue')
    ax_jsd.plot(common_amounts, interpolated_cdf_bank, label='Without Mortgage', color='red', linestyle='--')
    ax_jsd.set_title('JSD on CDFs')
    ax_jsd.legend()

    # Hellinger Distance Plot
    kde_with_mortgage = gaussian_kde(bank_with_mortgage_df['Amount'])
    kde_bank = gaussian_kde(bank_df['Amount'])
    kde_values_with_mortgage = kde_with_mortgage(common_amounts)
    kde_values_bank = kde_bank(common_amounts)
    hellinger_kde = hellinger_distance(kde_values_with_mortgage, kde_values_bank)
    score_kde = 1 - hellinger_kde
    fig_hd, ax_hd = plt.subplots()
    ax_hd.plot(common_amounts, kde_values_with_mortgage, label='With Mortgage KDE', color='blue')
    ax_hd.plot(common_amounts, kde_values_bank, label='Without Mortgage KDE', color='red', linestyle='--')
    ax_hd.set_title('Hellinger Distance KDE')
    ax_hd.legend()


    # Financial score calculation
    totalassets = propertyassets + nonpropertyassets
    networth = totalassets - totalliabilities
    financialassets = nonpropertyassets - totalliabilities

    titeratio = (totalannualincome + proposedannualrent) / (totalannualcommitments + totalinterestpayment)
    nalaratio = proposedloanamount / networth
    na24iratio = networth / totalinterestpayment
    fa24iratio = financialassets / totalinterestpayment

    # Scores calculation (titescore, nalascore, na24iscore, fa24iscore)
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
    score_financial = financialscore * 0.2

    # Calculate the Credit Score as the average of all scores
    credit_score = (inverted_score_ks + score_mwu + score_jsd_cdf + score_kde + score_financial) / 5

    # Create Polar Chart for Scores
    labels=np.array(['K-S Test', 'Mann-Whitney U', 'JSD', 'Hellinger Distance', 'Financial Score'])
    stats=np.array([inverted_score_ks, score_mwu, score_jsd_cdf, score_kde, score_financial])

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    stats=np.concatenate((stats,[stats[0]]))
    angles+=angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='green', alpha=0.25)
    ax.plot(angles, stats, color='green', linewidth=2)  # Draw the outline of our data
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Credit Score:")
        st.subheader("Financial Score:")

    with col2:
        # Display the original credit score
        st.markdown(f"<h2 style='text-align: left; color: red; margin: 0; padding: 0;'>{credit_score:.4f}</h2>", unsafe_allow_html=True)
        # Display the new financial score
        st.markdown(f"<h2 style='text-align: left; color: red; margin: 0; padding: 0;'>{financialscore:.4f}</h2>", unsafe_allow_html=True)

    st.pyplot(fig)

    # Streamlit layout for other plots in 2x2 grid
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("K-S Test")
        st.text(f"Score: {inverted_score_ks:.4f}")
        st.pyplot(fig_ks)

        st.subheader("Jensen-Shannon Divergence")
        st.text(f"Score: {score_jsd_cdf:.4f}")
        st.pyplot(fig_jsd)

    with col2:
        st.subheader("Mann-Whitney U Test")
        st.text(f"Score: {score_mwu:.4f}")
        st.pyplot(fig_mw)

        st.subheader("Hellinger Distance")
        st.text(f"Score: {score_kde:.4f}")
        st.pyplot(fig_hd)

else:
    st.warning("Please upload both files to proceed.")
