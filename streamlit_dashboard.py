import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

TRANSACTIONS_FILE = "finance-tracker/database/transactions.txt"

# --- Helper Functions ---
def _load_transactions():
    transactions = []

    # If no file exists → return empty df
    if not os.path.exists(TRANSACTIONS_FILE):
        return pd.DataFrame(columns=["Date", "Type", "Amount", "Category/Source", "Description", "Amount_Display"])

    # Read stored transactions
    with open(TRANSACTIONS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 5:
                transactions.append({
                    "Date": datetime.strptime(parts[0], "%Y-%m-%d").date(),
                    "Type": parts[1],
                    "Amount": int(parts[2]),
                    "Category/Source": parts[3],
                    "Description": parts[4]
                })

    # Convert list to DataFrame
    df = pd.DataFrame(transactions)

    # FIX: SAFE AMOUNT DISPLAY COLUMN
    df["Amount_Display"] = df["Amount"].apply(lambda x: f"Rs {x / 100:.2f}")

    # Sort by latest date
    return df.sort_values(by="Date", ascending=False)


def _save_transaction(transaction_type, amount_paisa, category_source, description, date):
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{date},{transaction_type},{amount_paisa},{category_source},{description}\n")


# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("💰 Personal Finance Tracker Dashboard")

# Sidebar Navigation
menu = ["Transactions", "Budgets", "Analytics"]
choice = st.sidebar.radio("Menu", menu)

# --- TRANSACTIONS PAGE ---
if choice == "Transactions":
    st.header("💸 Transaction Management")

    tab1, tab2, tab3 = st.tabs(["Add Transaction", "View Transactions", "Monthly Balance"])

    # ---------------- TAB 1: Add Transaction ----------------
    with tab1:
        st.subheader("Add New Transaction")
        transaction_type = st.radio("Select Type", ["Expense", "Income"])

        with st.form("add_transaction_form", clear_on_submit=True):
            amount_str = st.text_input("Amount (e.g., 12.50)", key="amount_input")

            if transaction_type == "Expense":
                categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
                category_source = st.selectbox("Select Category", categories)
            else:
                sources = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]
                category_source = st.selectbox("Select Income Source", sources)

            description = st.text_area("Description", key="description_input")
            date = st.date_input("Date", datetime.now())

            submitted = st.form_submit_button("Add Transaction")

            if submitted:
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        st.error("Amount must be positive.")
                    else:
                        amount_paisa = int(amount * 100)
                        _save_transaction(transaction_type.lower(), amount_paisa, category_source, description, date.strftime("%Y-%m-%d"))
                        st.success("Transaction added successfully!")
                except ValueError:
                    st.error("Invalid amount. Please enter a number.")

    # ---------------- TAB 2: View Transactions ----------------
    with tab2:
        st.subheader("View All Transactions")
        df_transactions = _load_transactions()

        if not df_transactions.empty:
            filter_option = st.selectbox(
                "Filter Transactions",
                ["All", "Last 7 Days", "Only Expenses", "Only Income"]
            )

            filtered_df = df_transactions.copy()
            if filter_option == "Last 7 Days":
                seven_days_ago = datetime.now().date() - timedelta(days=7)
                filtered_df = filtered_df[filtered_df["Date"] >= seven_days_ago]
            elif filter_option == "Only Expenses":
                filtered_df = filtered_df[filtered_df["Type"] == "expense"]
            elif filter_option == "Only Income":
                filtered_df = filtered_df[filtered_df["Type"] == "income"]

            # Style amounts
            def color_amount(row):
                if row["Type"] == "expense":
                    return ['color: red'] * len(row)
                else:
                    return ['color: green'] * len(row)

            st.dataframe(
                filtered_df.style.apply(color_amount, axis=1, subset=["Amount_Display"])
            )
        else:
            st.info("No transactions recorded yet.")

    # ---------------- TAB 3: Monthly Balance ----------------
    with tab3:
        st.subheader("Monthly Balance")
        df_transactions = _load_transactions()

        if not df_transactions.empty:
            current_month = datetime.now().strftime("%Y-%m")
            monthly_transactions = df_transactions[df_transactions["Date"].apply(lambda x: x.strftime("%Y-%m")) == current_month]

            total_income = monthly_transactions[monthly_transactions["Type"] == "income"]["Amount"].sum()
            total_expenses = monthly_transactions[monthly_transactions["Type"] == "expense"]["Amount"].sum()
            balance = total_income - total_expenses

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"Rs {total_income / 100:.2f}", delta_color="off")
            col2.metric("Total Expenses", f"Rs {total_expenses / 100:.2f}", delta_color="off")
            if balance >= 0:
                col3.metric("Current Balance", f"Rs {balance / 100:.2f}", delta="", delta_color="off")
            else:
                col3.metric("Current Balance", f"Rs {balance / 100:.2f}", delta="", delta_color="inverse")
        else:
            st.info("No transactions for the current month yet.")


# --- BUDGET PAGE ---
elif choice == "Budgets":
    st.header("💰 Budget Management")
    st.info("Budget management features are under development.")

# --- ANALYTICS PAGE ---
elif choice == "Analytics":
    st.header("📊 Financial Analytics")
    st.info("Financial analytics features are under development.")
