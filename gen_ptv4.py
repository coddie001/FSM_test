import pandas as pd

# Load the CSV file
filename = 'FSM_PTV.xlsx'
df = pd.read_excel(filename, sheet_name=None)

# Load sheets
reference_sheet = df['Sheet1']
gwk_1_sheet = df['gwk_1']
game_weeks = [df[f'gwk_{i}'] for i in range(1, 35)]

# Step 1: Update the game week points in the reference sheet
for col in reference_sheet.columns[3:]:
    reference_sheet[col] *= 10

# Remove the extra row with the total sum for gwk_points
#gwk_points =   # Exclude the last row

# Step 2: Calculate total game week points for each game week
total_gwk_points = reference_sheet.iloc[:, 3:].sum()
reference_sheet['Total Points'] = total_gwk_points

# Helper function for calculations
def calculate_values(gwk_points, previous_new_ptv):
    base_price = previous_new_ptv * 38
    pv_ratio = gwk_points / base_price
    p_g_wac = gwk_points * pv_ratio
    m_g_wac = p_g_wac.mean()
    deviation = p_g_wac - m_g_wac
    new_ptv = previous_new_ptv + deviation
    new_price = new_ptv * 38
    return base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price

# Initialize previous_new_ptv from gwk_1
previous_new_ptv = gwk_1_sheet.iloc[5, 2:37].values

# Create a dictionary to store data for each game week
gwk_data = {}

# Ensure the lengths match
gwk_points=reference_sheet.columns[3:][:-1].values
base_price=gwk_1_sheet.columns[1:,:1].values
if len(gwk_points) != len(base_price):
    raise ValueError("Input arrays must have the same length after removing the extra row")

# Process each game week
for i in range(2, 35):
    gwk_points = reference_sheet.iloc[:, i+3].values
    #gwk_points = df['gwk_points']
    base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price = calculate_values(gwk_points, previous_new_ptv)

    gwk_data[f'gwk_{i}'] = {
        'player_name': reference_sheet['player_name'].tolist(),
        'base_price': base_price.tolist(),
        'pv_ratio': pv_ratio.tolist(),
        'p_g_wac': p_g_wac.tolist(),
        'deviation': deviation.tolist(),
        'new_ptv': new_ptv.tolist(),
        'new_price': new_price.tolist()
    }
    
    previous_new_ptv = new_ptv

# Write the results to a new CSV file
output_filename = 'Final_FSM_New_PTV.csv'
with open(output_filename, 'w') as f:
    for i in range(2, 35):
        sheet_data = gwk_data[f'gwk_{i}']
        df_output = pd.DataFrame({
            'player_name': sheet_data['player_name'],
            'base_price': sheet_data['base_price'],
            'pv_ratio': sheet_data['pv_ratio'],
            'p_g_wac': sheet_data['p_g_wac'],
            'deviation': sheet_data['deviation'],
            'new_ptv': sheet_data['new_ptv'],
            'new_price': sheet_data['new_price']
        })
        df_output.to_csv(f, index=False, header=True, mode='a')
