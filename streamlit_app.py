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
1. **Number Guessing Game**  
   Test your guessing skills in a fun and interactive game.

2. **Dynamic ATM Simulation**  
   Analyze the behavior of customers interacting with an ATM system.

3. **Biased Dice Rolls**  
   Explore and visualize how biased probabilities affect dice rolls.

4. **Monte Carlo Dice Simulation**  
   Dive into Monte Carlo methods with dice roll experiments.

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

# Optional: Add an image or placeholder
st.image("https://via.placeholder.com/800x200.png?text=Simulation+App", caption="Enjoy exploring the simulations!")
