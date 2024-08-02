import pandas as pd
import random
from datetime import datetime, timedelta

# Load the initial data
df = pd.read_csv("FSM_Trade.csv", header=None, names=["gamer", "player"])

# Extract gamers and players
gamers = df["gamer"].dropna().tolist()
players = df["player"].dropna().tolist()

# Define stake ranges for different gamer groups
gamer_stake_ranges = [
    {"range": (5, 250), "gamers": gamers[0:200]},
    {"range": (250, 750), "gamers": gamers[200:800]},
    {"range": (750, 2500), "gamers": gamers[800:1000]}
]

# Define maximum total value for players based on their index
player_value_limits = [10000] * 11 + [15000] * 18 + [25000] * 6

def generate_trades_for_player(player, player_index, num_weeks=16):
    trades = []
    start_date = datetime.today()
    total_buy_volume = 0
    total_sell_volume = 0
    total_value = 0

    # Ensure ALL first trades are buys (one per gamer)
    for gamer_group in gamer_stake_ranges:
        gamer = random.choice(gamer_group["gamers"])
        trade_datetime = start_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
        amount = random.randint(gamer_group["range"][0], gamer_group["range"][1])
        total_buy_volume += amount
        total_value += amount

        trade = {
            "date": trade_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "gamer": gamer,
            "trade_type": "buy",
            "amount": amount,
            "player": player
        }
        trades.append(trade)

    # Generate remaining trades
    for week in range(num_weeks):
        num_trades = random.randint(10, 20)  # Increased weekly trades per player (10-20)
        for _ in range(num_trades):
            gamer_group = random.choice(gamer_stake_ranges)
            gamer = random.choice(gamer_group["gamers"])
            trade_datetime = start_date + timedelta(weeks=week, days=random.randint(0, 6), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
            trade_type = "sell" if random.random() < 0.5 and total_buy_volume > total_sell_volume else "buy"

            if trade_type == "buy":
                amount = random.randint(gamer_group["range"][0], gamer_group["range"][1])
                if total_value + amount > player_value_limits[player_index]:
                    continue  # Skip this trade if it exceeds the total value limit
                total_buy_volume += amount
                total_value += amount
            else:
                max_sell_amount = min(gamer_group["range"][1], total_buy_volume - total_sell_volume)
                if max_sell_amount <= gamer_group["range"][0] or total_value - max_sell_amount < 0:
                    continue  # Skip this trade if max_sell_amount is not in the valid range or it exceeds the total value limit
                amount = -random.randint(gamer_group["range"][0], max_sell_amount)
                total_sell_volume += abs(amount)
                total_value += amount

            trade = {
                "date": trade_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "gamer": gamer,
                "trade_type": trade_type,
                "amount": amount,
                "player": player
            }
            trades.append(trade)

    return trades

# Collect all trades
all_trades = []

task_count = 0
total_tasks = len(players)

# Process each player individually
for index, player in enumerate(players):
    print(f"Processing player {index + 1}/{total_tasks}: {player}")
    player_trades = generate_trades_for_player(player, index)
    all_trades.extend(player_trades)
    task_count += 1
    print(f"Progress: {task_count}/{total_tasks} tasks completed.")

# Convert the trades list to a DataFrame
df_all_trades = pd.DataFrame(all_trades)

# Save the data to a CSV file
df_all_trades.to_csv("TSW2_FSM_Trade.csv", index=False)

print("Task completed. Data exported to 'TSW5_FSM_Trade.csv'")