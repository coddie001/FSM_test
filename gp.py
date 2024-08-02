import csv
import random


def generate_random_numbers(reference_value, range_min, range_max):
  """
  Generates a list of 30 random whole numbers within the specified range,
  with a sum close to the reference value (within 10 units).
  """
  total_sum = 0
  numbers = []
  for _ in range(35): 
    while total_sum < reference_value - 10:
        new_number = random.randint(range_min, range_max)
        numbers.append(new_number)
        total_sum += new_number

  # Adjust the last number to ensure the sum is within the desired range
  if total_sum > reference_value + 10:
    numbers[-1] -= (total_sum - reference_value)
  elif total_sum < reference_value:
    numbers[-1] += (reference_value - total_sum)

  return numbers


def analyze_csv(filename):
  """
  Reads the CSV file, generates random numbers based on criteria,
  and writes the modified data to a new CSV file.
  """
  try:
    with open(filename, "r") as csvfile, open("modified_" + filename, "w", newline="") as new_csvfile:
      reader = csv.reader(csvfile)
      writer = csv.writer(new_csvfile)

      # Skip the header row
      next(reader)

      # Process each row
      for row in reader:
        player_name = row[0]  # Player name is in cell A (index 0)

        # Extract cell B value (mixed data types)
        cell_b_value = row[1].lower().strip()

        # Handle empty cell B
        if not cell_b_value:
            print(f"Warning: Empty value in cell B for row {player_name}")
            continue

        try:
            # Attempt conversion to integer for numeric values
            reference_cell = int(cell_b_value)
        except ValueError:
            # Use cell B value as string identifier for non-numeric values
            reference_cell = cell_b_value

        # Define range based on cell B value (modify as needed)
        if isinstance(reference_cell, int):  # Check if reference_cell is an integer
            if reference_cell >= 68 and reference_cell <= 111:
                range_min, range_max = 2, 7  # Numbers between 2 and 7 (inclusive)
            elif reference_cell >= 112 and reference_cell <= 158:
                range_min, range_max = 4, 15  # Numbers between 8 and 13 (inclusive)
            elif reference_cell >= 159 and reference_cell <= 245:
                range_min, range_max = 5, 22  # Numbers between 14 and 19 (inclusive)
            else:
                print(f"Warning: Unmatched range '{reference_cell}' in cell B for {player_name}")
                continue  # Skip rows with unmatched numeric ranges
        else:  # Use string identifier for non-numeric reference_cell
            # Define ranges based on string identifiers (modify as needed)
            if reference_cell == "b1":  # Example string identifier and range
                range_min, range_max = 60, 250
            else:
                print(f"Warning: Unmatched string identifier '{reference_cell}' in cell B for {player_name}")
                continue  # Skip rows with unmatched string identifiers

        # Generate random numbers
        random_numbers = generate_random_numbers(reference_cell, range_min, range_max)

        # Insert generated numbers into columns E-AH (indices 4-13)
        row.extend(random_numbers)

        # Write the modified row to the new CSV file
        writer.writerow(row)

  except FileNotFoundError:
      print(f"Error: File '{filename}' not found. Please check the file path.")


# Define ranges for random numbers based on cell location or string identifiers (modify as needed)
ranges = {
    # Numeric ranges (example)
    2: (2, 7),
    12: (8, 13),
    22: (14, 19),
    }
analyze_csv("FSM_GP.csv")
print("Analysis complete! Modified data is saved in 'modified_FSM_GP.csv'")