import os
import glob

START_YEAR = 2000
END_YEAR = 2025

SDC_RAW_DATA_FOLDER = f'SDC_{START_YEAR}-{END_YEAR}'
INTERMEDIATE_FOLDER = 'intermediate_output'

COUNTRY_INTEGRATION_FILE_PREFIX = f"SDC_{START_YEAR}-{END_YEAR}"
FILTERED_FILE_PREFIX = f"SDC_exclude_non_ipos_{START_YEAR}-{END_YEAR}"

IPO_FILTER_CRITERIA = {
    'keep_true': [
        'Original IPO Flag',
        'Main Tranche within Package flag'
    ],
    'exclude_true': [
        'Blank Check (SPAC) Involvement Y/N:',
        'Unit Issues: Unit Issue Flag',
        'Depositary Issue Flag',
        'Closed-end Fund/Trust Flag',
        'Fund or Trust Issue Flag',
        'Limited Partnership Flag (Y/N)',
        'Private Placement Flag'
    ],
    'exclude_not_empty': [
        'Issuer/Borrower REIT Type'
    ],
    'exclude_specific_value': {
        'Spinoff (Equity Carveout) Type (Code)': 'P'
    }
}

def get_existing_files(prefix):
    search_pattern = os.path.join(INTERMEDIATE_FOLDER, f"{prefix}_*.xlsx")
    return glob.glob(search_pattern)

def get_latest_file(prefix):
    # Automatically find the latest modified file with a specific prefix (ignoring record count suffix) in case of multiple matches
    files = get_existing_files(prefix)
    
    if not files:
        raise FileNotFoundError(f"File with prefix '{prefix}' not found. Please run the corresponding script first.")
        
    return max(files, key=os.path.getmtime)

def get_output_path(prefix, record_count):
    return os.path.join(INTERMEDIATE_FOLDER, f"{prefix}_{record_count}.xlsx")
