import streamlit as st

# Title of the App
st.title("Welcome to the Simulation App! 🚀")

# Introduction Section
st.markdown("""
### About This App
This application features a collection of interactive simulations designed for learning and analysis.  
Explore each simulation and discover the power of interactive problem-solving.

---

### 📚 Simulations Available:
1. **Number Guessing Simulation**  
   Explore the behavior of a number guessing simulation. Adjust parameters such as the range of numbers and the number of attempts to observe different strategies and outcomes. The simulation provides real-time feedback and statistical analysis of your guessing attempts, helping you understand common pitfalls and strategies to improve your guessing accuracy. Experiment with different settings to see how they affect the game dynamics and optimize your guessing technique.

2. **Dynamic ATM Simulation**  
   Dive into the ATM world with this simulation. Analyze the behavior of customers interacting with an ATM system, including transaction success rates, withdrawal patterns, and queue dynamics. This simulation helps in understanding real-world ATM usage scenarios and identifying potential areas for improvement.

3. **Biased Dice Rolls**  
   Explore and visualize how biased probabilities affect dice rolls. Adjust weights to simulate biased dice and observe the impact on outcomes. The simulation provides detailed statistics and graphical analysis, helping you understand how biases can influence random events.

4. **Monte Carlo Dice Simulation**  
   Dive into Monte Carlo methods with dice roll experiments. Adjust the number of dice, rolls, and biases to simulate various scenarios. This simulation helps in understanding the statistical principles behind Monte Carlo methods and their applications in decision-making and risk assessment.

---

### 🔍 How to Use:
- Navigate between simulations using the **sidebar menu**.
- Each simulation is in its own section for easy exploration.
- Customize parameters, run simulations, and view real-time results.

---

### ✨ Start Exploring!
Use the sidebar to select a simulation and begin your journey. Each section is designed to be intuitive and interactive, catering to learners and enthusiasts alike.
""")

# Footer Section
st.markdown("---")
st.info("💡 **Tip:** Make sure to adjust parameters to fully explore each simulation!")
st.write("**Developed by Your Name | Powered by Streamlit**")
