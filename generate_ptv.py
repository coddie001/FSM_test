import pandas as pd
import numpy as np

# Load the Excel file
filename = 'FSM_PTV.xlsx'
xls = pd.ExcelFile(filename)

# Load sheets
reference_sheet = pd.read_excel(xls, sheet_name='Sheet1')
gwk_1_sheet = pd.read_excel(xls, sheet_name='gwk_1')

# Create a dictionary for game weeks 2 to 34
game_weeks = {f'gwk_{i}': pd.read_excel(xls, sheet_name=f'gwk_{i}') for i in range(2, 35)}

# Step 1: Update game week points by multiplying by 10
reference_sheet.iloc[:, 4:] = reference_sheet.iloc[:, 4:] * 10

# Step 2: Calculate total game week points for each week
total_gwk_points = reference_sheet.iloc[:, 4:].sum()

# Step 3: Initialize calculations
def calculate_gwk_values(gwk_points, previous_new_ptv):
    base_price = previous_new_ptv * 38
    pv_ratio = gwk_points / base_price
    p_g_wac = gwk_points * pv_ratio
    m_g_wac = p_g_wac.mean()
    deviation = p_g_wac - m_g_wac
    new_ptv = previous_new_ptv + deviation
    new_price = new_ptv * 38
    return base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price

# Extract player names and initial values
player_names = reference_sheet['player_name'].tolist()
initial_new_ptv = gwk_1_sheet.iloc[5, 2:37].values

# Dictionary to store results
gwk_data = {}

# Calculate values for each game week
for i in range(2, 35):
    # Debugging print statements
    print(f"Processing Game Week {i}")



    gwk_points = reference_sheet.iloc[:, :].values
    
    try:
        base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price = calculate_gwk_values(gwk_points, initial_new_ptv)
    except Exception as e:
        print(f"Error calculating values for Game Week {i}: {e}")
        continue
    
    gwk_data[f'gwk_{i}'] = {
        'player_name': player_names,
        'base_price': base_price.tolist(),
        'pv_ratio': pv_ratio.tolist(),
        'p_g_wac': p_g_wac.tolist(),
        'deviation': deviation.tolist(),
        'new_ptv': new_ptv.tolist(),
        'new_price': new_price.tolist()
    }
    
    initial_new_ptv = new_ptv

# Write data to a new Excel file
output_filename = 'Final_FSM_New_PTV.xlsx'
with pd.ExcelWriter(output_filename) as writer:
    # Write reference sheet and gwk_1 sheet
    reference_sheet.to_excel(writer, sheet_name='Sheet1', index=False)
    gwk_1_sheet.to_excel(writer, sheet_name='Sheet2', index=False)
    
    # Write each game week data
    for i in range(2, 35):
        sheet_name = f'gwk_{i}'
        data = gwk_data.get(sheet_name, {})
        
        if not data:
            continue
        
        sheet_data = pd.DataFrame({
            'player_name': data.get('player_name', []),
            'base_price': data.get('base_price', []),
            'pv_ratio': data.get('pv_ratio', []),
            'p_g_wac': data.get('p_g_wac', []),
            'deviation': data.get('deviation', []),
            'new_ptv': data.get('new_ptv', []),
            'new_price': data.get('new_price', [])
        })
        
        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Write total game week points
    total_points_df = pd.DataFrame(total_gwk_points).T
    total_points_df.columns = reference_sheet.columns[4:]
    total_points_df.index = ['Total Points']
    total_points_df.to_excel(writer, sheet_name='Sheet1', startrow=len(reference_sheet) + 2, index=False)

print("Processing complete. Results saved to:", output_filename)
