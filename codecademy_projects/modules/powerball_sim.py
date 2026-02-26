import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------------
# Settings
# ------------------------
TICKET_COST = 2

PRIZES = {
    (5, True): 292_200_000,  # Jackpot
    (5, False): 1_000_000,
    (4, True): 50_000,
    (4, False): 100,
    (3, True): 100,
    (3, False): 7,
    (2, True): 7,
    (1, True): 4,
    (0, True): 4,
}

JACKPOT_ODDS = 1 / 292_201_338

# Real-world statistical comparisons
STAT_FACTS = [
    ("being struck by lightning this year", 1 / 500_000),
    ("die from a shark attack", 1 / 3_748_067),
    ("die from a dog bite", 1 / 112_400_000),
    ("die from a bear attack", 1 / 2_100_000),
    ("die from a crocodile attack", 1 / 1_500_000),
    ("die from a lion attack", 1 / 1_000_000),
    ("being murdered in the US", 1 / 18_000),
    ("getting a royal flush in poker", 1 / 649_740),
    ("being dealt the same poker hand twice in a row", 1 / 422_000_000),
]

# ANSI colors for terminal
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# ------------------------
# Functions
# ------------------------
def generate_ticket():
    white = set(random.sample(range(1, 70), 5))
    red = random.randint(1, 26)
    return white, red

def fun_statistical_fact():
    event, odds = random.choice(STAT_FACTS)
    comparison = JACKPOT_ODDS / odds
    if comparison < 1:
        return f"You are more likely to {event} than win the Powerball jackpot."
    else:
        return f"You are less likely to {event} than win the Powerball jackpot."

def simulate_powerball_with_topups(initial_credit, weekly_spend, weeks_per_year, years):
    total_weeks = weeks_per_year * years
    balance = initial_credit
    balance_history = []
    total_spent_history = []
    total_won_history = []
    total_spent = 0
    total_won = 0

    for week in range(1, total_weeks + 1):
        if balance < weekly_spend:
            print(f"\nWeek {week}: Insufficient balance (${balance}) for weekly spend ${weekly_spend}.")
            action = input("Do you want to top up (t), skip week (s), or quit simulation (q)? [t/s/q]: ").lower()
            if action == 't':
                extra = float(input("Enter top-up amount ($): "))
                balance += extra
                print(f"New balance: ${balance}")
            elif action == 's':
                print("Skipping this week due to insufficient funds.")
                balance_history.append(balance)
                total_spent_history.append(total_spent)
                total_won_history.append(total_won)
                continue
            elif action == 'q':
                print("Quitting simulation...")
                break
            else:
                print("Invalid input. Skipping this week by default.")
                balance_history.append(balance)
                total_spent_history.append(total_spent)
                total_won_history.append(total_won)
                continue

        tickets_to_buy = int(weekly_spend // TICKET_COST)
        total_spent += tickets_to_buy * TICKET_COST
        balance -= tickets_to_buy * TICKET_COST

        winning_white, winning_red = generate_ticket()
        weekly_won = 0
        for _ in range(tickets_to_buy):
            ticket_white, ticket_red = generate_ticket()
            white_matches = len(ticket_white & winning_white)
            red_match = (ticket_red == winning_red)
            prize = PRIZES.get((white_matches, red_match), 0)
            if prize > 0:
                weekly_won += prize

        balance += weekly_won
        total_won += weekly_won
        balance_history.append(balance)
        total_spent_history.append(total_spent)
        total_won_history.append(total_won)

        # Highlight big wins
        if weekly_won >= 1_000_000:
            print(f"🎉 HUGE WIN in Week {week}! Won ${weekly_won}")

        print(f"Week {week}: Spent ${tickets_to_buy*TICKET_COST}, Won ${weekly_won}, Balance ${balance}")

    net_profit = total_won - total_spent
    total_lost = total_spent - total_won if total_spent > total_won else 0
    return balance_history, total_spent_history, total_won_history, total_spent, total_won, net_profit, total_lost

# ------------------------
# User Inputs
# ------------------------
initial_credit = float(input("Enter starting credit ($): "))
weekly_spend = float(input("Enter weekly spend ($): "))

weeks_input = input("Enter number of weeks per year (press Enter for 52): ")
weeks_per_year = int(weeks_input) if weeks_input.strip() else 52

years = int(input("Enter number of years to simulate: "))

# ------------------------
# Run Simulation
# ------------------------
balance_history, spent_history, won_history, total_spent, total_won, net_profit, total_lost = simulate_powerball_with_topups(
    initial_credit, weekly_spend, weeks_per_year, years
)

# ------------------------
# Summary with Highlights
# ------------------------
final_balance = balance_history[-1]

print("\n--- Simulation Summary ---")
print(f"Initial Credit: ${initial_credit}")
print(f"Weeks per Year: {weeks_per_year}")
print(f"Years Simulated: {years}")
print(f"Total Weeks Simulated: {len(balance_history)}")
print(f"Total Spent: ${total_spent}")
print(f"Total Won: ${total_won}")
print(f"Total Lost: ${total_lost}")
print(f"Net Profit/Loss: ${net_profit}")
print(f"Final Balance: ${final_balance}")
print("#" * 100)  # Divider between balance and jackpot/fun fact

# Highlight jackpot chance
print(f"{BOLD}{CYAN}Chance of winning the Powerball jackpot: 1 in 292,201,338{RESET}")

# Fun Fact in yellow
print(f"{YELLOW}Fun Fact: {fun_statistical_fact()}{RESET}")

# ------------------------
# Animated Graph
# ------------------------
show_graph = input("\nDo you want to see the animated balance graph? (y/n): ").lower()
if show_graph == 'y':
    fig, ax = plt.subplots(figsize=(14,7))
    ax.set_title(f"🎲 Powerball Simulation: Balance over {years} Years", fontsize=16)
    ax.set_xlabel("Week Number")
    ax.set_ylabel("Balance ($)")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(0, len(balance_history))
    min_balance = min(balance_history + [initial_credit])
    max_balance = max(balance_history + [initial_credit])
    ax.set_ylim(min_balance*0.9, max_balance*1.1)

    def animate(i):
        ax.clear()
        ax.plot(range(i+1), balance_history[:i+1], color='green', linewidth=2, label='Balance')
        # Shaded profit/loss areas
        ax.fill_between(range(i+1), initial_credit, balance_history[:i+1], 
                        where=[b>=initial_credit for b in balance_history[:i+1]], 
                        color='green', alpha=0.2, interpolate=True)
        ax.fill_between(range(i+1), initial_credit, balance_history[:i+1], 
                        where=[b<initial_credit for b in balance_history[:i+1]], 
                        color='red', alpha=0.2, interpolate=True)
        ax.set_xlim(0, len(balance_history))
        ax.set_ylim(min_balance*0.9, max_balance*1.1)
        ax.set_xlabel("Week Number")
        ax.set_ylabel("Balance ($)")
        ax.set_title(f"🎲 Powerball Simulation: Balance over {years} Years", fontsize=16)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()

    ani = FuncAnimation(fig, animate, frames=len(balance_history), interval=50, repeat=False)
    plt.show()
else:
    print("Graph skipped. Simulation complete.")