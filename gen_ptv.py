import pandas as pd
import numpy as np

def process_fsm_ptv(file_path):
    """Processes the FSM_PTV.csv file and creates a new CSV with calculated values.

    Args:
        file_path (str): Path to the FSM_PTV.csv file.
    """

    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=None)

    # Process Sheet 1
    sheet1 = df['Sheet1']
    gwk_cols = [f'gwk_{i}' for i in range(1, 35)]
    sheet1[gwk_cols] *= 10
    sheet1['total_points'] = sheet1[gwk_cols].sum(axis=1)

    # Skip the first row
    sheet1 = sheet1.iloc[1:]

    # Process Sheet 2 (gwk_1)
    sheet2 = df['gwk_1']
    num_players = sheet2.shape[0] - 1  # Exclude header column

    # Assuming row names are consistent
    player_name_row = 'player_name'
    base_price_row = 'base_price'
    pv_ratio_row = 'pv_ratio'
    p_g_wac_row = 'p_g_wac'
    deviation_row = 'deviation'
    new_ptv_row = 'new_ptv'
    new_price_row = 'new_price'

    # Define row indices for header rows
    base_price_row = sheet2.index[sheet2['player_name'] == 'base_price'][1]
    new_ptv_row = sheet2.index[sheet2['player_name'] == 'new_ptv'][1]
    new_price_row = sheet2.index[sheet2['player_name'] == 'new_price'][1]

    # Starting column for gwk data
    gwk_start_col = 4

    # Create output DataFrames
    output_dfs = {}

    # Process game weeks 2 to 34
    for gwk in range(2, 35):
        previous_gwk_sheet = df[f'gwk_{gwk-1}']

        # Create output DataFrame
        output_df = pd.DataFrame(columns=[player_name_row, base_price_row, pv_ratio_row, p_g_wac_row, deviation_row, new_ptv_row, new_price_row])

        # Iterate over players
        for player in range(2, num_players + 2):  # Start from row 2
            base_price = previous_gwk_sheet.iloc[new_price_row, player - 1]
            pv_ratio = sheet1.iloc[player - 1, gwk] / base_price
            p_g_wac = pv_ratio * sheet1.iloc[player - 1, gwk]
            m_g_wac = p_g_wac.sum() / num_players
            deviation = p_g_wac - m_g_wac
            new_ptv = previous_gwk_sheet.iloc[new_ptv_row, player - 1] + deviation
            new_price = new_ptv * 38

            output_df.loc[player - 1] = [player - 1, base_price, pv_ratio, p_g_wac, deviation, new_ptv, new_price]

        output_dfs[f'Sheet{gwk}'] = output_df

    # Save the new CSV file
    with pd.ExcelWriter('FSM_New_PTV.xlsx') as writer:
        for sheet_name, df in output_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            if __name__ == "__main__":
                file_path = "FSM_PTV.xlsx"  # Assuming Excel file
    process_fsm_ptv(file_path)
    print("FSM_New_PTV.xlsx file created successfully.")