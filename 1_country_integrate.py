import os
import glob
import sys
import pandas as pd
import config
import utility

output_path = config.COUNTRY_INTEGRATION_PATH

# Check if the output file already exists and ask for overwrite permission
if os.path.exists(output_path):
    user_response = input(f"{output_path} already exists. Do you want to overwrite it? (Y/N): ")
    if user_response.lower() != 'y':
        print("Operation cancelled.")
        exit()

# Find all Excel files in the specific folder
search_pattern = os.path.join(config.SDC_RAW_DATA_FOLDER, '*.xlsx')
excel_files = glob.glob(search_pattern)

# Skip SDC_IPO_variables_2000-2025.xlsx since it is the output file in the same folder
excel_files = [
    file for file in excel_files 
    if os.path.basename(file) != os.path.basename(config.COUNTRY_INTEGRATION_PATH)
    and not os.path.basename(file).startswith('~$')
]

# Sort files in alphabetical order
excel_files.sort()

df_list = []

for current_file in excel_files:
    file_name = os.path.basename(current_file)
    print(f"Processing: {file_name} ...", end=" ")

    try:
        # Read data from 'Request 3' sheet with row 3 as column names
        current_df = pd.read_excel(current_file, sheet_name='Request 3', header=2)
        current_df = utility.convert_datetime_to_date(current_df)

        df_list.append(current_df)
        print("Done")
    except Exception as error:
        print(f"FAILED! Skipped due to error: {error}")
        sys.exit()

combined_df = pd.concat(df_list, ignore_index=True)

# Fill all empty values with a dot
combined_df = combined_df.fillna('.')

combined_df.to_excel(output_path, index=False)
print("All countries merge completed successfully.")
