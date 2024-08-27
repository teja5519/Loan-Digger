import streamlit as st
import openai
import math
import csv
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
#from Loan_Amortization_Schedule import calculate_emi
from Loan_Amortization_Schedule import create_amortization_schedule
#from Loan_Amortization_Schedule import visualize_data
from Sensitivity_Analysis import sensitivity_analysis
from Sensitivity_Analysis import visualize_sensitivity
from Loan_terms import calculate_loan_term
from Loan_terms import create_loan_terms_amortization_schedule
from Loan_terms import visualize_data
#from Account import app


import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

def detect_mobile_device():
    # Your mobile device detection logic here
    # Return True if mobile, False otherwise
    return False  # Placeholder



def main():
    st.title("Loan Digger")



    with st.expander("About Loan Digger"):
        st.write("This app Helps you understand your loan better.")
        st.write("Explore Amortization, sensitivity analysis, and loan term calculation.")
    # Create a sidebar for additional options
    #st.sidebar.header("Loan Digger Options")
    #show_advanced_options = st.sidebar.checkbox("Show Advanced Options")
    # Main content area
    col1, col2 = st.columns([2, 1])
    with col1:
        
        # Tabbed interface
        tab1, tab2, tab3,  = st.tabs([ "Amortization", "Sensitivity Analysis", "EMI - EXPLORE your MORTGAGE INTELLIGENTLY"])
    
    with col2:
     # Additional information or visualizations
        st.header("")
        # Display calculated values or other relevant information

        # Conditional content based on checkbox
        # if show_advanced_options:
        #     st.subheader("Advanced Options")
        #     # Add advanced options here, e.g.,
        #     chart_type = st.radio("Chart Type:", ("Bar", "Line"))
    


        
    

    with tab1:
        # Input fields
        principal = st.slider("Principal Amount (P) ", min_value=1000, max_value=10000000, value=50000, step=1000, help="The Initial amount borrowed.")
        rate = st.slider("Interest Rate (%)", min_value=0.0, max_value=25.0, value=7.3, step=0.01, help="The Annual Interest Rate")
        years = st.slider("Loan Tenure (Years)", min_value=1, max_value=25, value=3, step=1, help= "The loan Duration in Years.")
        


        if st.button("Calculate your loan schedule"):
            progress_bar = st.progress(0)
            for i in range(100):
               progress_bar.progress(i + 1)
            time.sleep(0.04)  # Simulate some work
            try:
                amortization_schedule = create_amortization_schedule(principal, rate, years)
                st.dataframe(amortization_schedule)
                visualize_data(amortization_schedule)
                # if st.button("Export Amortization Schedule"):
                #   export_to_csv(amortization_schedule, "Amortization_Schedule.csv")
            except ValueError as e:
                st.error(e)

    with tab2:
        rate_range_min = st.number_input("Minimum Interest Rate for Sensitivity Analysis (%)", value=rate * 0.8, step=0.25, help="The lowest interest rate to consider in the sensitivity analysis")
        rate_range_max = st.number_input("Maximum Interest Rate for Sensitivity Analysis (%)", value=rate * 1.2, step=0.25, help="The highest interest rate to consider in the sensitivity analysis.")
        years_range_min = st.number_input("Minimum Loan Term for Sensitivity Analysis (years)", value=years - 1, step=1, help="The shortest loan term to consider in the sensitivity analysis.")
        years_range_max = st.number_input("Maximum Loan Term for Sensitivity Analysis (years)", value=years + 1, step=1, help="The longest loan term to consider in the sensitivity analysis.")

        if st.button("Calculate your loan Sensitivity"):
            progress_bar = st.progress(0)
            for i in range(100):
               progress_bar.progress(i + 1)
            time.sleep(0.04)  # Simulate some work
            try:
                sensitivity_results = sensitivity_analysis(principal, rate, years, rate_range_min, rate_range_max, years_range_min, years_range_max)
                visualize_sensitivity(sensitivity_results)
                # if st.button("Export Sensitivity Analysis"):
                #  export_to_csv(sensitivity_results, "Sensitivity_analysis.csv")
            except ValueError as e:
                st.error(e)

    with tab3:
        PMT = st.number_input("Monthly Payment (PMT)", min_value=100, step=500, help="The Amount your plan to pay each month.")
        r = st.number_input("Monthly Interest Rate (r)", min_value=0.0, step=0.01, help="The Interest Rate applied monthly.(For Example, To calculate your monthly rate= ( your loan Annual rate / 12)") / (12 * 100)
        P = st.number_input("Principal Amount (P)", min_value=100, max_value=10000000, step=1000, help="The Initial Amount you borrowed.")

        if st.button("Calculate Loan Term"):
            progress_bar = st.progress(0)
            for i in range(100):
               progress_bar.progress(i + 1)
            time.sleep(0.04)  # Simulate some work
            try:
                loan_term = calculate_loan_term(PMT, r, P)
                st.write(f"Number of months to clear the loan is: {loan_term:.2f}")
                loan_terms_schedule = create_loan_terms_amortization_schedule(PMT, r, P)
                st.dataframe(loan_terms_schedule)
                visualize_data(loan_terms_schedule)

            except ValueError as e:
              st.error(e)

    # with tab4:
    #     st.write()
    #     #app()



if __name__ == "__main__":
  main()


