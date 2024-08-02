import pandas as pd

# Load the CSV file
xls = pd.ExcelFile('FSM_PTV.xlsx')

# Load the reference sheet and the first game week sheet
reference_sheet = pd.read_excel(xls, sheet_name='Sheet1')
gwk_1_sheet = pd.read_excel(xls, sheet_name='gwk_1')

# Exclude the first row from the reference sheet
reference_sheet = reference_sheet.iloc[1:, :]

# Multiply the game week points by 10 in the reference sheet
for col in reference_sheet.columns[3:]:
    reference_sheet[col] = reference_sheet[col] * 10

# Function to calculate values for each game week
def calculate_gwk_values(gwk_points, previous_new_ptv):
    base_price = previous_new_ptv * 38
    pv_ratio = gwk_points / base_price
    p_g_wac = gwk_points * pv_ratio
    m_g_wac = p_g_wac.mean()
    deviation = p_g_wac - m_g_wac
    new_ptv = previous_new_ptv + deviation
    new_price = new_ptv * 38
    return base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price

# Create a dictionary to store data for each game week
gwk_data = {f'gwk_{i}': {} for i in range(2, 35)}

# Extract player names from the reference sheet
player_names = reference_sheet.iloc[:, 0].values  # Assuming player names are in the first column

# Initialize previous_new_ptv with values from gwk_1
previous_new_ptv = gwk_1_sheet.iloc[5, 2:36].values  # Adjusted to 34 elements

# Calculate values for each game week and store in gwk_data
for i in range(2, min(35, reference_sheet.shape[1] - 3)):  # i+3 must be <= 36
    print(f"Processing game week: gwk_{i}")
    print(f"Accessing column index: {i+3}")
    
    # Check if column index is within bounds
    if i+3 < reference_sheet.shape[1]:
        gwk_points = reference_sheet.iloc[:, i+3].values
        base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price = calculate_gwk_values(gwk_points, previous_new_ptv)
        
        gwk_data[f'gwk_{i}'] = {
            'player_name': player_names,  # Store player names
            'base_price': base_price,
            'pv_ratio': pv_ratio,
            'p_g_wac': p_g_wac,
            'deviation': deviation,
            'new_ptv': new_ptv,
            'new_price': new_price
        }
        
        previous_new_ptv = new_ptv
    else:
        print(f"Column index {i+3} is out of bounds")

# Debug print to check gwk_data contents
for i in range(2, 35):
    print(f"Contents of gwk_data[f'gwk_{i}']:")
    print(gwk_data[f'gwk_{i}'])

# Write data to each game week sheet
with pd.ExcelWriter('FSM_New_PTV.xlsx') as writer:
    reference_sheet.to_excel(writer, sheet_name='Sheet1', index=False)
    gwk_1_sheet.to_excel(writer, sheet_name='Sheet2', index=False)
    
    for i in range(2, 35):
        sheet_name = f'gwk_{i}'
        if f'gwk_{i}' in gwk_data:
            if 'player_name' in gwk_data[f'gwk_{i}']:  # Ensure 'player_name' exists
                sheet_data = pd.DataFrame({
                    'player_name': gwk_data[f'gwk_{i}']['player_name'],
                    'base_price': gwk_data[f'gwk_{i}']['base_price'],
                    'pv_ratio': gwk_data[f'gwk_{i}']['pv_ratio'],
                    'p_g_wac': gwk_data[f'gwk_{i}']['p_g_wac'],
                    'deviation': gwk_data[f'gwk_{i}']['deviation'],
                    'new_ptv': gwk_data[f'gwk_{i}']['new_ptv'],
                    'new_price': gwk_data[f'gwk_{i}']['new_price']
                })
                # Save to Excel
                sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                print(f"Key 'player_name' not found in gwk_data for {sheet_name}")
        else:
            print(f"Game week {sheet_name} not found in gwk_data")
