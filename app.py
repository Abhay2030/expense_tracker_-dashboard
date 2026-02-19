import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from data_handler import initialize_file, add_transaction, get_all_transactions

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Expense Tracker", page_icon="📈", layout="wide")

initialize_file()

# --- AUTHENTICATION STATE ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def login_screen():
    st.title("Admin Login")
    st.markdown("Please enter your credentials to access the financial dashboard.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # Hardcoded admin credentials for demonstration
            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid username or password.")

def main_dashboard():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Dashboard", "Add Transaction", "View All Transactions"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    # --- DATA LOADING ---
    transactions = get_all_transactions()
    df = pd.DataFrame(transactions)
    
    if not df.empty:
        # Clean and prepare data for the UI
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['date'] = pd.to_datetime(df['date'])

    # --- VIEW: DASHBOARD ---
    if menu == "Dashboard":
        st.title("Admin Dashboard")
        
        if df.empty:
            st.info("No transaction data available. Please add some records first.")
            return

        # Calculate metrics for the current month
        current_month = datetime.now().strftime("%Y-%m")
        monthly_df = df[df['date'].dt.strftime("%Y-%m") == current_month]
        
        income = monthly_df[monthly_df['type'] == 'income']['amount'].sum()
        expense = monthly_df[monthly_df['type'] == 'expense']['amount'].sum()
        savings = income - expense

        # Display top metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Income", f"₹{income:,.2f}")
        col2.metric("Monthly Expense", f"₹{expense:,.2f}")
        col3.metric("Net Savings", f"₹{savings:,.2f}")
        
        st.markdown("---")
        
        # Display Graph
        st.subheader("Expense Breakdown by Category")
        expense_df = df[df['type'] == 'expense']
        if not expense_df.empty:
            cat_summary = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            cat_summary.plot(kind='bar', ax=ax, color='#ff4b4b')
            ax.set_ylabel("Amount")
            ax.set_xlabel("Category")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.info("No expenses recorded yet to show a graph.")

    # --- VIEW: ADD TRANSACTION ---
    elif menu == "Add Transaction":
        st.title("Add New Transaction")
        
        with st.form("transaction_form"):
            t_type = st.selectbox("Transaction Type", ["expense", "income"])
            amount = st.number_input("Amount", min_value=0.01, format="%.2f")
            category = st.text_input("Category / Source (e.g., Food, Salary, Rent)")
            
            submitted = st.form_submit_button("Save Record")
            
            if submitted:
                if category.strip() == "":
                    st.error("Category cannot be empty.")
                else:
                    add_transaction(t_type, amount, category.strip().lower())
                    st.success(f"Successfully added {t_type} of ₹{amount:,.2f} under '{category}'.")

    # --- VIEW: ALL TRANSACTIONS ---
    elif menu == "View All Transactions":
        st.title("Transaction History")
        if not df.empty:
            # Render a clean, sortable table
            st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No transactions found.")

# --- ROUTER ---
if not st.session_state["logged_in"]:
    login_screen()
else:
    main_dashboard()