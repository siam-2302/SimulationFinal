import random
import matplotlib
matplotlib.use('Agg')  # Ensure correct backend for Streamlit
import matplotlib.pyplot as plt
import streamlit as st

# Define global variables
attempts = []
guesses = []

# Function for guessing simulation
def guess(mode, num_range):
    secret_number = random.randint(1, num_range)
    low = 1
    high = num_range
    attempt = 0
    found = False

    st.info(f"Secret number selected between 1 and {num_range}. Start guessing!")

    # Progress bar in Streamlit
    progress_bar = st.progress(0)
    while not found:
        # Guess logic
        if mode == "Random Guess Mode":
            current_guess = random.randint(low, high)
        elif mode == "Binary Search Mode":
            current_guess = (low + high) // 2
        elif mode == "Ternary Search Mode":
            mid1 = low + (high - low) // 3
            mid2 = high - (high - low) // 3
            if secret_number < mid1:
                current_guess = low + (mid1 - low) // 2
            elif secret_number > mid2:
                current_guess = high - (high - mid2) // 2
            else:
                current_guess = (mid1 + mid2) // 2
        elif mode == "Golden Ratio Search Mode":
            golden_ratio = 0.618
            mid = int(low + golden_ratio * (high - low))
            current_guess = mid

        # Record data
        attempt += 1
        attempts.append(attempt)
        guesses.append(current_guess)

        # Update progress bar
        progress_bar.progress(min((abs(current_guess - secret_number) / num_range), 1.0))

        # Evaluate guess
        if current_guess == secret_number:
            st.success(f"Success! Guessed the number {secret_number} in {attempt} attempts!")
            found = True
        elif current_guess < secret_number:
            st.warning(f"Guess {current_guess} is too low.")
            low = current_guess + 1
        else:
            st.warning(f"Guess {current_guess} is too high.")
            high = current_guess - 1

        # Plot progress
        plot_progress(mode, attempt, current_guess, low, high, num_range)

    # Print summary
    print_summary(secret_number, attempt, mode)

def plot_progress(mode, attempt, current_guess, low, high, num_range):
    st.subheader("Simulation Progress")
    plt.figure(figsize=(10, 5))
    plt.plot(attempts, guesses, 'b-o', label="Guesses")
    plt.axhline(low, color='g', linestyle='--', label="Lower Bound")
    plt.axhline(high, color='r', linestyle='--', label="Upper Bound")
    plt.scatter(attempt, current_guess, color='orange', zorder=5, label=f"Current Guess: {current_guess}")
    plt.xlabel('Attempts')  
    plt.ylabel('Guesses')  
    plt.title(f"{mode}\nTotal Attempts: {attempt}")  
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def print_summary(secret_number, attempt, mode):
    st.subheader("Simulation Summary")
    st.write(f"Secret Number: {secret_number}")
    st.write(f"Total Attempts: {attempt}")
    st.write(f"Mode Used: {mode}")
    avg_guess = sum(guesses) // len(guesses)
    st.write(f"Average Guess: {avg_guess}")

# Streamlit App Layout
def main():
    st.title("Guessing Simulation")

    # User inputs
    mode = st.selectbox("Choose the guessing mode", [
        "Random Guess Mode",
        "Binary Search Mode",
        "Ternary Search Mode",
        "Golden Ratio Search Mode"
    ])
    num_range = st.number_input("Enter the range of numbers (e.g., 100000)", min_value=1, value=100000)

    if st.button("Start Simulation"):
        # Reset global variables
        attempts.clear()
        guesses.clear()
        guess(mode, num_range)

if __name__ == "__main__":
    main()
