import random
import time
from datetime import datetime
import streamlit as st

# Utility functions
def random_divisible_by_100(min_val, max_val):
    return random.randint(min_val // 100, max_val // 100) * 100

def print_timestamp():
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

# Classes
class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.transactions = []

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"- Withdrawn ${amount} ({print_timestamp()})")
            return True
        else:
            self.transactions.append(f"- Failed Withdraw ${amount} (Insufficient Balance) ({print_timestamp()})")
        return False

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"+ Deposited ${amount} ({print_timestamp()})")

class ATM:
    def __init__(self, atm_id, cash_balance):
        self.atm_id = atm_id
        self.cash_balance = cash_balance
        self.enabled = True
        self.transactions = []

    def dispense_cash(self, amount):
        if self.cash_balance >= amount:
            self.cash_balance -= amount
            self.transactions.append(f"- Dispensed ${amount} ({print_timestamp()})")
            return True
        else:
            self.enabled = False
            return False

# Simulation function
def simulate_atm(customers, atms, max_iterations=None):
    successful_transactions = 0
    failed_transactions = 0
    total_attempts = 0
    total_time = 0
    iteration = 0
    maintenance_schedule = random.randint(1, 5)

    while any(atm.enabled for atm in atms) and (max_iterations is None or iteration < max_iterations):
        iteration += 1
        for customer in customers:
            if not any(atm.enabled for atm in atms):
                st.warning("All ATMs are out of cash or disabled. Simulation ends.")
                print_summary(customers, atms, successful_transactions, failed_transactions, total_attempts, total_time)
                return

            atm = random.choice([atm for atm in atms if atm.enabled])
            action = random.choice(["withdraw", "deposit"])
            if action == "withdraw":
                amount_to_process = random_divisible_by_100(1000, 5000)
                start_time = time.time()
                st.write(f"{print_timestamp()} {customer.name} approaches ATM-{atm.atm_id} to withdraw ${amount_to_process}")

                if random.random() < 0.05:
                    st.error(f"{print_timestamp()} ATM-{atm.atm_id} went out of service unexpectedly.")
                    atm.enabled = False
                    failed_transactions += 1
                    continue

                if customer.balance < amount_to_process:
                    st.warning(f"{print_timestamp()} Insufficient balance for {customer.name} to withdraw ${amount_to_process}")
                    failed_transactions += 1
                elif atm.cash_balance < amount_to_process:
                    st.warning(f"{print_timestamp()} ATM-{atm.atm_id} is out of cash. {customer.name}'s transaction failed.")
                    atm.enabled = False
                    failed_transactions += 1
                else:
                    customer.withdraw(amount_to_process)
                    atm.dispense_cash(amount_to_process)
                    end_time = time.time()
                    transaction_time = end_time - start_time
                    total_time += transaction_time
                    total_attempts += 1
                    st.success(f"{print_timestamp()} Transaction successful! {customer.name} withdrew ${amount_to_process} in {transaction_time:.2f} seconds")
            elif action == "deposit":
                amount_to_deposit = random_divisible_by_100(100, 5000)
                customer.deposit(amount_to_deposit)
                st.success(f"{print_timestamp()} {customer.name} deposited ${amount_to_deposit}")

            if iteration % maintenance_schedule == 0:
                atm.enabled = False
                st.warning(f"{print_timestamp()} ATM-{atm.atm_id} is undergoing maintenance.")
                time.sleep(1)
                atm.enabled = True
                st.success(f"{print_timestamp()} ATM-{atm.atm_id} is back online.")

            time.sleep(0.5)

    print_summary(customers, atms, successful_transactions, failed_transactions, total_attempts, total_time)

# Summary function
def print_summary(customers, atms, successful_transactions, failed_transactions, total_attempts, total_time):
    avg_transaction_time = total_time / total_attempts if total_attempts > 0 else 0

    st.markdown("\n### Simulation Summary")
    st.markdown(f"- **Total Successful Transactions:** {successful_transactions}")
    st.markdown(f"- **Total Failed Transactions:** {failed_transactions}")
    st.markdown(f"- **Total Attempts:** {total_attempts}")
    st.markdown(f"- **Average Transaction Time:** {avg_transaction_time:.2f} seconds")

    st.markdown("\n### ATM Statistics")
    for atm in atms:
        st.markdown(f"**ATM-{atm.atm_id}:**")
        st.markdown(f"  - Cash Balance: ${atm.cash_balance}")
        st.markdown(f"  - Transactions:")
        for transaction in atm.transactions:
            st.markdown(f"    {transaction}")

    st.markdown("\n### Customer Statistics")
    for customer in customers:
        st.markdown(f"**Customer-{customer.name}:**")
        st.markdown(f"  - Balance: ${customer.balance}")
        st.markdown(f"  - Transactions:")
        for transaction in customer.transactions:
            st.markdown(f"    {transaction}")

# Streamlit App UI
st.title("ATM Simulation")

# Sidebar Controls
st.sidebar.header("Simulation Settings")

# Instructions
st.sidebar.markdown("""
### Instructions:
1. Select the number of customers and ATMs for the simulation.
2. Set a maximum number of iterations (leave empty for unlimited).
3. Click "Start Simulation" to begin.
4. You can reset the simulation anytime.
""")

# Inputs
num_customers = st.sidebar.number_input("Number of Customers:", min_value=1, max_value=50, value=10)
num_atms = st.sidebar.number_input("Number of ATMs:", min_value=1, max_value=10, value=3)
max_iterations = st.sidebar.number_input("Maximum Iterations (optional):", min_value=1, value=20, step=1, format="%d")

# Buttons in Sidebar
if st.sidebar.button("Start Simulation"):
    customers = [Customer(f"Customer-{i}", random_divisible_by_100(2000, 10000)) for i in range(num_customers)]
    atms = [ATM(i, random_divisible_by_100(5000, 10000)) for i in range(num_atms)]
    simulate_atm(customers, atms, max_iterations=max_iterations)

if st.sidebar.button("Reset Simulation"):
    st.sidebar.write("Simulation reset. Ready to start again!")
