import csv
import random


def generate_random_numbers(reference_value, range_min, range_max):
  """
  Generates a list of 30 random whole numbers within the specified range,
  with a sum close to the reference value (within 10 units).
  """
  total_sum = 0
  numbers = []
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

      # Process each row (excluding the first 35 for header)
      for row in reader:
        cell_b_value = row[1].lower().strip()  # Get cell B value, lowercase, and remove whitespace
        if not cell_b_value:  # Check if cell B is empty
            print(f"Warning: Empty value in cell B for row {row}")
            continue  # Skip rows with empty cell B

        reference_cell = int(row[1])  # Assuming the reference value is in cell 3 (index 2)
        # Define range based on cell B value (modify ranges as needed)
        if "b2" <= cell_b_value <= "b11":
            range_min, range_max = ranges["b2"]
        elif "b12" <= cell_b_value <= "b21":
            range_min, range_max = ranges["b12"]
        elif "b22" <= cell_b_value <= "b36":
            range_min, range_max = ranges["b22"]
        else:
            # Handle unmatched ranges (e.g., print a warning)
            print(f"Warning: Unmatched range '{cell_b_value}' in row {row}")
            continue  # Skip rows with unmatched ranges

        # Generate random numbers
        random_numbers = generate_random_numbers(reference_cell, range_min, range_max)

        # Insert generated numbers into columns E-AH (indices 4-13)
        row.extend(random_numbers)

        # Write the modified row to the new CSV file
        writer.writerow(row)

  except FileNotFoundError:
      print(f"Error: File '{filename}' not found. Please check the file path.")


# Define ranges for random numbers based on cell location (modify as needed)
ranges = {
    "68": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "71": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "79": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "85": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "87": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "89": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "98": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "107": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "111": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "112": (2, 7),  # Numbers between 2 and 7 (inclusive)
    "115": (4, 15),  # Numbers between 4 and 15 (inclusive)
    "116": (4, 15),  # Numbers between 4 and 15 (inclusive)
    "117": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "123": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "132": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "133": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "137": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "146": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "149": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "159": (4, 15),  # Numbers between 5 and 22 (inclusive)
    "164": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "165": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "180": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "183": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "213": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "226": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "230": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "244": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "217": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "211": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "153": (5, 22),  # Numbers between 5 and 22 (inclusive)
    "127": (5, 22),  # Numbers between 5 and 22 (inclusive)
    }
analyze_csv("FSM_GP.csv")
print("Analysis complete! Modified data is saved in 'modified_FSM_GP.csv'")