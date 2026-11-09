import os
import glob
import re

START_YEAR = 2000
END_YEAR = 2025

SDC_RAW_DATA_FOLDER = f'SDC_{START_YEAR}-{END_YEAR}'
INTERMEDIATE_FOLDER = 'intermediate_output'

COUNTRY_INTEGRATION_FILE_PREFIX = f"SDC_{START_YEAR}-{END_YEAR}"

# Verbose regex for filenames with named groups
FILENAME_PATTERN = re.compile(
    r"""
    ^
    (?:
        (?P<country>[A-Z][A-Za-z]+(?:-[A-Z][A-Za-z]+)*)  # Match countries (e.g., Germany, South-Korea)
        |
        (?P<category>[A-Za-z0-9\-]+)                                     # Match categories (e.g., financial-return, non-life-insurance-1)
    )
    (?P<company>\d+)?               # Optional digit(s) for company number
    [_-]                            # Separator (underscore or hyphen)
    (?:(?!\d{4}(?:[-_]|$)).*?[_-])? # Optional intermediate text (e.g., quarterly-financial_), avoiding start year consumption
    (?P<start_year>\d{4})           # 4-digit start year
    (?:[-_](?P<end_year>\d{4}))?    # Optional hyphen/underscore and 4-digit end year
    (?:_(?P<suffix>[A-Za-z]+))?     # Optional suffix, e.g., "_A"
    (?:\.xlsm)?$                    # File extension
    """,
    re.VERBOSE
)

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
