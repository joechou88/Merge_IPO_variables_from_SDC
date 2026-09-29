import os

SDC_RAW_DATA_FOLDER = 'SDC_IPO_variables_2000-2025'
INTERMEDIATE_FOLDER = 'intermediate_output'

COUNTRY_INTEGRATION_PATH = os.path.join(INTERMEDIATE_FOLDER, f"{SDC_RAW_DATA_FOLDER}.xlsx")
FILTERED_IPO_PATH = os.path.join(INTERMEDIATE_FOLDER, "SDC_IPO_variables_exclude_non_ipos_2000-2025.xlsx")

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
