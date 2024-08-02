import pandas as pd

# Load the data
df = pd.read_csv("Sat_FSM_Trade.csv")

# Convert 'timestamp' and 'date' columns to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Filter the DataFrame for a specific player
df_salah = df[df['player'] == 'salah']

# Sort the DataFrame by date and timestamp
df_salah_sorted = df_salah.sort_values(by=['date', 'timestamp'], ascending=True)

# Display the first few rows of the sorted data
print(df_salah_sorted.head(500).to_string(index=False))

#print (df.head(500).to_string(index=False))



