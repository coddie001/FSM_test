import pandas as pd
import random

def filter_and_export(FSM):
  """
  Analyzes the given CSV file, filters values based on "z_scores" and exports a new CSV.

  Args:
    filename: The name of the CSV file to analyze (e.g., "FSM.csv").
  """

  # Read the CSV file into a pandas DataFrame
  df = pd.read_csv(FSM)

  # Filter data by z_scores ranges
  filtered_df = pd.DataFrame({
      "player": [],
      "z_scores": [],
  })

  # Select 10 random values from each z_score range (0-0.99, 1.0-1.99, 2.0-4.99)
  for lower, upper in [(0, 0.99), (1.0, 1.99), (2.0, 4.99)]:
    filtered_data = df[(df["z_scores"] >= lower) & (df["z_scores"] <= upper)]
    selected_data = filtered_data.sample(10, random_state=42)  # Set random state for reproducibility
    filtered_df = pd.concat([filtered_df, selected_data])

  # Sort the DataFrame by "z_scores"
  filtered_df = filtered_df.sort_values(by=["z_scores"])

  # Export the filtered data to a new CSV file (FSM_SORTED.csv)
  filtered_df.to_csv("FSM_SORTED.csv", index=False)

  print("Filtered data exported to FSM_SORTED.csv")

# Set the filename for analysis
filename = "FSM.csv"
filter_and_export(filename)