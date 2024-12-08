import streamlit as st
import random
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from time import sleep

# Define dice faces
dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

# Function to simulate biased dice rolls with animation
def simulate_biased_dice_rolls(num_dice, weights):
    st.write(f"Simulating {num_dice} dice rolls with custom weights...")
    rolls = []
    for _ in range(num_dice):
        roll = random.choices(dice_faces, weights=weights)[0]
        rolls.append(roll)
        # Display rolls in batches of 10 to save space
        if len(rolls) % 10 == 0:
            st.text(", ".join(rolls[-10:]))  # Show last 10 rolls
            sleep(0.5)  # Short delay to simulate rolling
    return rolls

# Function to calculate dice statistics
def calculate_statistics(sorted_dice):
    dice_values = [dice_faces.index(face) + 1 for face in sorted_dice]
    frequency = Counter(sorted_dice)
    dice_sum = sum(dice_values)
    dice_mean = np.mean(dice_values)
    dice_median = np.median(dice_values)
    mode_face, mode_count = frequency.most_common(1)[0]
    most_common = frequency.most_common(1)[0]
    least_common = frequency.most_common()[-1]
    return {
        "frequency": frequency,
        "sum": dice_sum,
        "mean": dice_mean,
        "median": dice_median,
        "mode": (mode_face, mode_count),
        "most_common": most_common,
        "least_common": least_common
    }

# Function to visualize dice roll distribution
def plot_dice_roll_distribution(frequency):
    fig, ax = plt.subplots()
    ax.bar(frequency.keys(), frequency.values(), color="skyblue", alpha=0.75)
    ax.set_xticks(range(1, 7))
    ax.set_xticklabels(dice_faces)
    ax.set_xlabel("Dice Face")
    ax.set_ylabel("Frequency")
    ax.set_title("Dice Roll Distribution")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Function to display streaks
def track_consecutive_streaks(sorted_dice):
    streaks = []
    current_streak = [sorted_dice[0]]
    
    for i in range(1, len(sorted_dice)):
        if sorted_dice[i] == sorted_dice[i - 1]:
            current_streak.append(sorted_dice[i])
        else:
            streaks.append(current_streak)
            current_streak = [sorted_dice[i]]
    
    streaks.append(current_streak)
    return streaks

# Streamlit app
def main():
    st.title("Biased Dice Rolls")
    st.sidebar.header("Simulation Settings")
    num_dice = st.sidebar.number_input("Number of Dice Rolls", min_value=1, max_value=1000, value=200)
    weights = [
        st.sidebar.slider(f"Weight for {face}", 0.0, 1.0, value, 0.1)
        for face, value in zip(dice_faces, [0.4, 0.2, 0.1, 0.1, 0.1, 0.1])
    ]

    if st.sidebar.button("Run Simulation"):
        st.subheader("Rolling the Dice...")
        rolls = simulate_biased_dice_rolls(num_dice, weights)
        sorted_rolls = sorted(rolls)

        # Display statistics at the top
        st.subheader("Statistics")
        stats = calculate_statistics(sorted_rolls)
        st.write(f"Sum: {stats['sum']}")
        st.write(f"Mean: {stats['mean']:.2f}")
        st.write(f"Median: {stats['median']:.2f}")
        st.write(f"Mode: {stats['mode'][0]} with {stats['mode'][1]} occurrences")
        st.write(f"Most Frequent: {stats['most_common'][0]} ({stats['most_common'][1]} occurrences)")
        st.write(f"Least Frequent: {stats['least_common'][0]} ({stats['least_common'][1]} occurrences)")

        st.subheader("Consecutive Streaks")
        streaks = track_consecutive_streaks(sorted_rolls)
        for i, streak in enumerate(streaks, 1):
            st.write(f"Streak {i}: {' '.join(streak)}")

        # Display the distribution graph at the bottom
        st.subheader("Dice Roll Distribution")
        plot_dice_roll_distribution(Counter(sorted_rolls))

    if st.sidebar.button("Reset Simulation"):
        st.write("Simulation reset. Ready to start again!")
        st.stop()  # Stops and clears the app state for a fresh simulation

if __name__ == "__main__":
    main()
