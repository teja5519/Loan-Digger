import streamlit as st
import math
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from Loan_Amortization_Schedule import calculate_emi

def sensitivity_analysis(principal, rate, years, rate_range_min, rate_range_max, years_range_min, years_range_max):
    """Performs sensitivity analysis on interest rate and loan term.

    Args:
        principal: The principal amount of the loan.
        rate: The annual interest rate.
        years: The loan tenure in years.

    Returns:
        A pandas DataFrame containing the sensitivity analysis results.
    """

    # Define ranges for sensitivity analysis
    rate_range = np.linspace(rate_range_min, rate_range_max, 10)
    years_range = np.arange(years_range_min, years_range_max + 1)

    results = []
    for r in rate_range:
        for y in years_range:
            emi = calculate_emi(principal, r, y)
            total_interest = emi * y * 12 - principal
            total_principal_paid = total_interest - emi + principal
            results.append([r, y, emi, total_interest, total_principal_paid])

    df_sensitivity = pd.DataFrame(results, columns=['Interest Rate', 'Loan Term (Years)', 'EMI', 'Total Interest Paid', 'Loan  Settled'])
    return df_sensitivity

def visualize_sensitivity(df_sensitivity):
    """Visualizes sensitivity analysis results."""

    # Display sensitivity analysis results as a table
    st.dataframe(df_sensitivity)

    # Interactive bubble chart
    fig = px.scatter(df_sensitivity, x='Interest Rate', y='Loan Term (Years)',
                     size='EMI', color='Total Interest Paid',
                     hover_name='EMI', size_max=60)
    fig.update_layout(title='Sensitivity Analysis: EMI and Total Interest')
    st.plotly_chart(fig)

    # Interactive 3D scatter plot
    fig = px.scatter_3d(df_sensitivity, x='Interest Rate', y='Loan Term (Years)', z='EMI',
                       color='Total Interest Paid',
                       hover_name='EMI')
    fig.update_layout(title='Sensitivity Analysis: 3D View')
    st.plotly_chart(fig)

