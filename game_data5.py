import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import math

# Constants
NUM_PLAYERS = 35
NUM_WEEKS = 16
MIN_TRADES_PER_WEEK = 10
MAX_TRADES_PER_WEEK = 20

# Read the CSV file
df = pd.read_csv('FSM_Trade.csv', header=None, names=['Gamer', 'Player'])

# Separate gamers and players
gamers = df['Gamer'].tolist()
players = df['Player'].unique()

# Define gamer ranges
gamer_ranges = {
    (0, 199): (5, 250),
    (200, 799): (250, 750),
    (800, 999): (750, 2500),
}

# Define player limits
player_limits = [
    10000,   # For players B1:B11
    15000,   # For players B12:B29
    25000    # For players B30:B35
]

# Function to generate random date and time
def random_datetime(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Function to generate trades
def generate_trades(player, player_index):
    player_start_date = datetime.now() - timedelta(weeks=NUM_WEEKS)
    player_end_date = datetime.now()

    # Determine the max value based on player index
    if 0 <= player_index < 11:
        max_total_value = player_limits[0]
    elif 11 <= player_index < 29:
        max_total_value = player_limits[1]
    else:
        max_total_value = player_limits[2]

    trades = []
    total_buy_value = 0
    total_sell_value = 0
    num_trades = random.randint(MIN_TRADES_PER_WEEK, MAX_TRADES_PER_WEEK) * NUM_WEEKS

    # Ensure first trade is a buy
    trades.append({
        'date': random_datetime(player_start_date, player_end_date),
        'gamer': random.choice(gamers),
        'trade_type': 'buy',
        'amount': random.randint(5, 2500),
        'last_market_cap': 0,
        'player': player
    })
    total_buy_value += trades[-1]['amount']

    for _ in range(num_trades - 1):
        trade_type = 'buy' if random.random() > 0.5 else 'sell'
        if trade_type == 'buy':
            amount = random.randint(5, 2500)
            if total_buy_value + amount > max_total_value:
                amount = max_total_value - total_buy_value
            total_buy_value += amount
        else:
            amount = -random.randint(5, 2500)
            if total_sell_value - amount < -total_buy_value:
                amount = -total_buy_value - total_sell_value
            total_sell_value += amount
        
        trades.append({
            'date': random_datetime(player_start_date, player_end_date),
            'gamer': random.choice(gamers),
            'trade_type': trade_type,
            'amount': amount,
            'last_market_cap': 0,
            'player': player
        })

    # Ensure the total sell volume/value does not exceed total buy volume/value
    while total_sell_value < -total_buy_value:
        for trade in trades:
            if trade['trade_type'] == 'sell' and trade['amount'] < 0:
                trade['amount'] = -total_buy_value - total_sell_value
                total_sell_value += trade['amount']
                break
    
    # Update last_market_cap
    last_market_cap = 0
    for trade in trades:
        if trade['trade_type'] == 'buy':
            last_market_cap += trade['amount']
        elif trade['trade_type'] == 'sell':
            if last_market_cap + trade['amount'] < 0:
                trade['amount'] = -last_market_cap
                last_market_cap = 0
            else:
                last_market_cap += trade['amount']
        trade['last_market_cap'] = last_market_cap

    return trades

# Create a Pandas Excel writer object
with pd.ExcelWriter('TSW2_FSM_Trade.xlsx') as writer:
    # Process each player
    for index, player in enumerate(players):
        print(f'Processing player {player} ({index + 1}/{NUM_PLAYERS})')
        trades = generate_trades(player, index)
        df_trades = pd.DataFrame(trades)
        df_trades.to_excel(writer, sheet_name=player, index=False)

print('All data has been written to TSW2_FSM_Trade.xlsx')
