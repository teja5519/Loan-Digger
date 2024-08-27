import streamlit as st
import math
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def calculate_emi(principal, rate, years):
  """Calculates the EMI for a loan.

  Args:
    principal: The principal amount of the loan.
    rate: The annual interest rate.
    years: The loan tenure in years.

  Returns:
    The EMI amount.
  """

  if principal <= 0 or rate < 0 or years <= 0:
    raise ValueError("Invalid input values. Principal, rate, and years must be positive.")

  monthly_interest_rate = rate / (12 * 100)
  months = years * 12
  emi = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)
  return emi

def create_amortization_schedule(principal, rate, years):
  """Creates an amortization schedule for a loan.

  Args:
    principal: The principal amount of the loan.
    rate: The annual interest rate.
    years: The loan tenure in years.

  Returns:
    A pandas DataFrame containing the amortization schedule.
  """

  emi = calculate_emi(principal, rate, years)
  monthly_interest_rate = rate / (12 * 100)
  months = years * 12

  data = []
  balance = principal
  for month in range(1, months + 1):
      interest_paid = balance * monthly_interest_rate
      principal_paid = emi - interest_paid
      balance -= principal_paid
      data.append([month, balance + principal_paid, emi, interest_paid, principal_paid, balance])

  df = pd.DataFrame(data, columns=["Month", "Beginning Balance", "EMI", "Interest Paid", "Principal Paid", "Ending Balance"])
  return df



