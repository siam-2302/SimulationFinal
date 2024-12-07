import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
from IPython.display import clear_output

attempts = []
guesses = []

def guess(mode):
    secret_number = random.randint(1, 100000)
    low = 1
    high = 100000
    attempt = 0
    found = False

    print(f"\n\033[96m[INFO] Secret number is randomly selected between 1 and 100,000.\033[0m\n")

    with tqdm(total=100000, desc="Guessing Progress", unit="step") as pbar:
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

            plot_progress(mode, attempt, current_guess, low, high)

            # Update progress bar
            pbar.update(abs(current_guess - secret_number))

            time.sleep(0.1)

            # Evaluate guess
            if current_guess == secret_number:
                print(f"\033[92mSuccess! Guessed the number {secret_number} in {attempt} attempts!\033[0m")
                found = True
            elif current_guess < secret_number:
                print(f"\033[94mGuess {current_guess} is too low.\033[0m")
                low = current_guess + 1
            else:
                print(f"\033[91mGuess {current_guess} is too high.\033[0m")
                high = current_guess - 1

    # Print summary
    print_summary(secret_number, attempt, mode)

def plot_progress(mode, attempt, current_guess, low, high):
    if not st.session_state.get('graph_shown', False):
        st.session_state['graph_shown'] = True
        
        clear_output(wait=True)

        mode_titles = {
            1: 'Random Guess Mode',
            2: 'Binary Search Mode',
            3: 'Ternary Search Mode',
            4: 'Golden Ratio Search Mode',
            5: 'Logarithmic Search Mode'
        }

        title = mode_titles.get(mode, 'Unknown Mode')

        plt.figure(figsize=(10, 5))
        plt.plot(attempts, guesses, 'b-o', label="Guesses")
        plt.axhline(low, color='g', linestyle='--', label="Lower Bound")
        plt.axhline(high, color='r', linestyle='--', label="Upper Bound")
        plt.scatter(attempt, current_guess, color='orange', zorder=5, label=f"Current Guess: {current_guess}")
        plt.xlabel('Attempts')  
        plt.ylabel('Guesses')  
        plt.title(f"{title}\nTotal Attempts: {attempt}")  
        plt.legend()
        plt.grid(True)
        plt.show()

def print_summary(secret_number, attempt, mode):
    print("\n\033[96m=== Simulation Summary ===\033[0m")
    print(f"Secret Number: \033[93m{secret_number}\033[0m")
    print(f"Total Attempts: \033[93m{attempt}\033[0m")
    print(f"Mode Used: \033[93m{mode}\033[0m")
    print(f"Average Guess: \033[93m{sum(guesses) // len(guesses)}\033[0m")
    print("\033[96m=========================\033[0m")

if __name__ == "__main__":
    while True:
        print("Choose the guessing mode:")
        print("1: Random Guess Mode")
        print("2: Binary Search Mode")
        print("3: Ternary Search Mode")
        print("4: Golden Ratio Search Mode")
        print("5: Logarithmic Search Mode")
        print("6: Exit")

        mode = int(input("Enter the mode (1, 2, 3, 4, 5, or 6): "))
        if mode == 6:
            print("Exiting the simulation. Goodbye!")
            break
        elif mode not in [1, 2, 3, 4, 5]:
            print("Invalid mode selected. Try again.")
        else:
            attempts.clear()
            guesses.clear()
            guess(mode)
