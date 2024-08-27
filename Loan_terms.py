import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 

def calculate_loan_term(PMT, r, P):
      """
  Calculates the number of months it will take to clear a loan.

  Args:
    PMT: The monthly payment amount.
    r: The monthly interest rate.
    P: The principal amount (loan amount).

  Returns:
    The number of months it will take to clear the loan.
  """

      if 1 - (r * P) / PMT <= 0:
            raise ValueError("Invalid input values. Loan payment cannot be equal to or less than the interest.")

      n = -math.log(1 - (r * P) / PMT) / math.log(1 + r)
      return n


def create_loan_terms_amortization_schedule(PMT, r, P):
    """
    Creates an amortization schedule based on the given loan parameters.

    Args:
        PMT: The monthly payment amount.
        r: The monthly interest rate.
        P: The principal amount (loan amount).

    Returns:
        A pandas DataFrame containing the amortization schedule.
    """

    n = calculate_loan_term(PMT, r, P)
    n = int(n)  # Convert to integer for indexing

    schedule = []
    balance = P
    for i in range(1, n + 1):
        interest_paid = balance * r
        principal_paid = PMT - interest_paid
        balance -= principal_paid
        schedule.append([i, balance, PMT, interest_paid, principal_paid, balance])

    df = pd.DataFrame(schedule, columns=["Month", "Beginning Balance", "PMT", "Interest Paid", "Principal Paid", "Ending Balance"])
    df['EMI'] = PMT  # Add EMI column
    return df




def visualize_data(df):
    """Visualizes the amortization schedule data.

    Args:
        df: The pandas DataFrame containing the amortization schedule.
    """

    # Create three columns
    col1, col2,  = st.columns(2)


    # Pie chart
    with col1:
        total_principal = df['Principal Paid'].sum()
        total_interest = df['Interest Paid'].sum()
        values = [total_principal, total_interest]
        names = ['Principal Paid', 'Interest Paid']
        fig1 = px.pie(values=values, names=names, title="Principal paid and Interest paid over the Entire loan term")
        st.plotly_chart(fig1)

    # Line chart
    with col2:
        fig2 = px.line(df, x='Month', y=['Principal Paid', 'Interest Paid', 'Beginning Balance'],
                     title='Principal, Interest, and Beginning Balance Over Time')
        st.plotly_chart(fig2)


