from locale import currency
import streamlit as st
import plotly.graph_objects as pgo
import calendar
from datetime import datetime

incomes = ["Salary","Investments","Other incomes"]
expenses = ["Utilities","Insurance","Groceries","Bills","Other expenses"]

currency = "INR"
page_title = "Income & Expense Tracker"
page_icon = ":alien:" 
layout = "centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_title + " " + page_icon)

years = [datetime.today().year - 1, datetime.today().year,  datetime.today().year + 1]
# print(years)
months = list(calendar.month_name[1:])
# print(months)

st.header(f"Data Entry in {currency}")
with st.form("entry_form", clear_on_submit=True):
    col1,col2 = st.columns(2)
    col1.selectbox("Select Month:", months, key="month")
    col1.selectbox("Select Year:", years, key="year")

    with st.expander("Income"):
        for income in incomes:
            st.number_input(f"{income}:", min_value=0, format="%i", step=1000,key=income)
    
    with st.expander("Expanses"):
        for expense in expenses:
            st.number_input(f"{expense}:", min_value=0, format="%i", step=100,key=expense)

    submitted = st.form_submit_button("Save Data")
    if submitted:
        period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
        incomes = {income: st.session_state[income] for income in incomes}
        expenses = {expense: st.session_state[expense] for expense in expenses}

        st.write(f"incomes: {incomes}")
        st.write(f"expenses: {expenses}")
        st.success("Data Saved")

    