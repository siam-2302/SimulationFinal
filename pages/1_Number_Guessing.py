import random
import matplotlib.pyplot as plt
import streamlit as st
import time

# Initialize global variables
attempts = []
guesses = []

# Function to perform guessing simulation
def guess(mode):
    secret_number = random.randint(1, 100000)
    low = 1
    high = 100000
    attempt = 0
    found = False

    st.info(f"[INFO] Secret number is randomly selected between 1 and 100,000.")
    progress_bar = st.progress(0)
    chart_placeholder = st.empty()  # Placeholder for the chart

    while not found:
        # Guess logic for each mode
        if mode == 1:  # Random Guess Mode
            current_guess = random.randint(low, high)
        elif mode == 2:  # Binary Search Mode
            current_guess = (low + high) // 2
        elif mode == 3:  # Ternary Search Mode
            mid1 = low + (high - low) // 3
            mid2 = high - (high - low) // 3
            if secret_number < mid1:
                current_guess = low + (mid1 - low) // 2
            elif secret_number > mid2:
                current_guess = high - (high - mid2) // 2
            else:
                current_guess = (mid1 + mid2) // 2
        elif mode == 4:  # Golden Ratio Search Mode
            golden_ratio = 0.618
            mid = int(low + golden_ratio * (high - low))
            current_guess = mid
        elif mode == 5:  # Logarithmic Search Mode
            current_guess = low + int((high - low) / (2 ** (attempt / 10 + 1)))

        # Record data
        attempt += 1
        attempts.append(attempt)
        guesses.append(current_guess)

        # Update progress
        progress = attempt / 100  # Simulate progress
        progress_bar.progress(min(progress, 1.0))  # Cap progress at 100%

        # Update the graph dynamically
        plot_progress(mode, attempt, current_guess, low, high, chart_placeholder)

        # Evaluate guess
        if current_guess == secret_number:
            st.success(f"🎉 Success! Guessed the number {secret_number} in {attempt} attempts!")
            found = True
        elif current_guess < secret_number:
            low = current_guess + 1
        else:
            high = current_guess - 1

    # Print summary
    print_summary(secret_number, attempt, mode)

# Plot progress function
def plot_progress(mode, attempt, current_guess, low, high, chart_placeholder):
    mode_titles = {
        1: 'Random Guess Mode',
        2: 'Binary Search Mode',
        3: 'Ternary Search Mode',
        4: 'Golden Ratio Search Mode',
        5: 'Logarithmic Search Mode'
    }
    title = mode_titles.get(mode, 'Unknown Mode')

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.plot(attempts, guesses, 'b-o', label="Guesses", markersize=4)
    plt.axhline(low, color='g', linestyle='--', label="Lower Bound")
    plt.axhline(high, color='r', linestyle='--', label="Upper Bound")
    plt.scatter(attempt, current_guess, color='orange', zorder=5, label=f"Current Guess: {current_guess}")
    plt.xlabel('Attempts')  
    plt.ylabel('Guesses')  
    plt.title(f"{title}\nAttempt: {attempt}, Current Guess: {current_guess}")  
    plt.legend()
    plt.grid(True)
    chart_placeholder.pyplot(plt)  # Use placeholder to update the chart
    plt.close()  # Prevent memory overflow
    time.sleep(0.1)  # Pause for animation effect

# Print summary
def print_summary(secret_number, attempt, mode):
    st.markdown(f"""
    ### Simulation Summary
    - **Secret Number:** {secret_number}
    - **Total Attempts:** {attempt}
    - **Mode Used:** {mode}
    - **Average Guess:** {sum(guesses) // len(guesses)}
    """)

# Streamlit App UI
st.title("Number Guessing Simulation")
st.sidebar.title("Choose Simulation Mode")

mode = st.sidebar.radio(
    "Select the guessing mode:",
    options=[
        "Random Guess Mode",
        "Binary Search Mode",
        "Ternary Search Mode",
        "Golden Ratio Search Mode",
        "Logarithmic Search Mode"
    ]
)

mode_mapping = {
    "Random Guess Mode": 1,
    "Binary Search Mode": 2,
    "Ternary Search Mode": 3,
    "Golden Ratio Search Mode": 4,
    "Logarithmic Search Mode": 5
}

if st.button("Start Simulation"):
    attempts.clear()
    guesses.clear()
    guess(mode_mapping[mode])
