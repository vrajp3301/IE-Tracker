from locale import currency
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as pgo
import calendar
from datetime import datetime

incomes = ["Salary","Investments","Other Incomes"]
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

hide_st_style = """
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Data","Data Visualization"],
    icons=["activity","bar-chart-fill"],
    orientation="horizontal"
)

if selected == "Data":
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
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_duration"):
        period = st.selectbox("Select Duration:", ["2022_March"])
        submitted = st.form_submit_button("Plot Duration")
        if submitted:
            incomes = {'Salary':70000,'Investments':50000,'Other Incomes': 0}
            expenses = {'Utilities':900,'Insurance':3000,'Groceries':300,'Bills':400,'Other expenses':500}

            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            rem_budget = total_income - total_expense
            
            col1,col2,col3 = st.columns(3)
            col1.metric("Total Income",f"{total_income} {currency}")
            col2.metric("Total Expense",f"{total_expense} {currency}")
            col3.metric("Budget Remaining",f"{rem_budget} {currency}")

            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())


            link = dict(source=source , target=target, value=value)
            node = dict(label=label, pad=20, thickness=20,color="#A0D995")
            data = pgo.Sankey(link=link, node=node)

            fig = pgo.Figure(data)
            fig.update_layout(margin=dict(l=0,r=0,t=5,b=5))
            st.plotly_chart(fig,use_container_width=True)
