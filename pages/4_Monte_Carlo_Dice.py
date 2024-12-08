import streamlit as st
import random
import matplotlib.pyplot as plt
from collections import Counter
import time

# Define colors and their biased probabilities
colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange']
biased_probs = {
    'Red': 0.3,
    'Blue': 0.2,
    'Green': 0.15,
    'Yellow': 0.15,
    'Purple': 0.1,
    'Orange': 0.1
}

# Function to roll multiple colored dice
def roll_multiple_dice(num_rolls, num_dice=1, biased=False):
    """Simulate rolling multiple colored dice"""
    rolls = []
    for _ in range(num_rolls):
        if biased:
            roll = random.choices(colors, weights=[biased_probs[color] for color in colors], k=num_dice)
        else:
            roll = random.choices(colors, k=num_dice)
        rolls.append(roll)
    return rolls

# Function to analyze and plot the distribution of dice rolls with animation
def analyze_and_plot(rolls, num_dice, biased):
    """Analyze and plot the distribution of dice rolls"""
    flat_rolls = [color for roll in rolls for color in roll]
    count = Counter(flat_rolls)
    probabilities = {color: count[color]/len(flat_rolls) for color in colors}

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_positions = range(len(colors))
    bar = ax.bar(probabilities.keys(), probabilities.values(), color=colors)

    # Add the theoretical distribution line
    theoretical_probs = [biased_probs[color] if biased else 1/len(colors) for color in colors]
    ax.plot(bar_positions, theoretical_probs, 'k--', label='Theoretical (Biased)' if biased else 'Theoretical (Fair)')
    ax.set_ylim(0, max(max(probabilities.values()), max(theoretical_probs)) + 0.05)
    ax.legend()
    ax.set_title('Probability Distribution of Colored Dice Rolls')
    ax.set_xlabel('Colors')
    ax.set_ylabel('Probability')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(colors)

    # Display the plot with animation
    for i in range(0, len(bar_positions), 1):
        bar[i].set_height(0)
        bar[i].set_color('grey')
        plt.pause(0.05)  # Short delay for animation effect

    for i, p in enumerate(probabilities.values()):
        bar[i].set_height(p)
        bar[i].set_color(colors[i])

    plt.show()
    st.pyplot(fig)

# Streamlit app
def main():
    if 'num_simulations' not in st.session_state:
        st.session_state.num_simulations = 10000
    if 'num_dice' not in st.session_state:
        st.session_state.num_dice = 3
    if 'biased' not in st.session_state:
        st.session_state.biased = True

    st.title("Monte Carlo Colored Dice Simulation")
    
    # Instructions
    st.sidebar.header("Instructions")
    st.sidebar.write("""
    - Use the settings in the sidebar to configure the simulation:
      - **Simulation Type**: Choose whether the dice rolls are biased or fair.
      - **Number of Simulations**: Adjust the number of times you want to roll the dice.
      - **Number of Dice per Simulation**: Choose how many dice will be rolled in each simulation.
    - Click **Run Simulation** to start the Monte Carlo simulation.
    - The results will display the probability distribution for each color.
    - Use **Reset Simulation** to start over with a fresh setup.
    - The theoretical distribution line will show the expected probabilities based on either biased or fair conditions.
    """)

    st.sidebar.header("Simulation Settings")
    st.session_state.biased = st.sidebar.radio("Simulation Type", ["Biased", "Fair"], index=0)
    st.session_state.num_simulations = st.sidebar.number_input("Number of Simulations", min_value=1, max_value=100000, value=st.session_state.num_simulations)
    st.session_state.num_dice = st.sidebar.number_input("Number of Dice per Simulation", min_value=1, max_value=6, value=st.session_state.num_dice)

    if st.sidebar.button("Run Simulation"):
        st.subheader("Running Simulation...")
        
        # Show statistics with delay for animation
        with st.spinner('Simulating...'):
            results = roll_multiple_dice(st.session_state.num_simulations, st.session_state.num_dice, biased=(st.session_state.biased == "Biased"))
            time.sleep(0.5)  # Simulate processing time
        
        # Show statistics first
        st.subheader("Simulation Statistics:")
        probabilities = Counter([color for roll in results for color in roll])
        for color, prob in probabilities.items():
            st.write(f"{color}: {prob/st.session_state.num_simulations:.4f}")

        # Show graph with animation
        st.subheader("Probability Distribution:")
        analyze_and_plot(results, st.session_state.num_dice, biased=(st.session_state.biased == "Biased"))

    if st.sidebar.button("Reset Simulation"):
        st.session_state.clear()
        st.success("Simulation reset. Ready to start again!")

if __name__ == "__main__":
    main()
