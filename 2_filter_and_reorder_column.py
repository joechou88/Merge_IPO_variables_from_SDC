import logging
import pandas as pd
from datetime import datetime
import config

# Setup logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"2_filter_and_reorder_column_{timestamp}.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Define the exact columns to keep and their order
target_columns = [
    "New Issues SEDOL",
    "ISIN",
    "Datastream",
    "Issuer/Borrower 9-digit CUSIP",
    "Issuer/Borrower Short Name",
    "Issuer/Borrower Name Full",
    "Dates: Issue Date",
    "Dates: Offer Year (CCYY)",
    "country",
    "country_code",
    "country_code2",
    "Issuer/Borrower Nation",
    "Issuer/Borrower Founded Date",
    "New Issues SDC Industry",
    "New Issues High Tech Industry Group",
    "New Issues Primary SIC (Code)",
    "Offer Price (USD)",
    "File Price, Mid (USD)",
    "Spinoff (Equity Carveout) Company: Pct Owned by Parent After Spinoff",
    "Global Offering: International Shares Offered",
    "Proceeds Amount All Markets (USD Millions)",
    "Bookrunner",
    "Offering Technique",
    "Pricing Technique",
    "Venture Capital Backed IPO Issue Flag",
    "Original IPO Flag",
    "Main Tranche within Package flag",
    "Blank Check (SPAC) Involvement Y/N:",
    "Unit Issues: Unit Issue Flag",
    "Depositary Issue Flag",
    "Issuer/Borrower REIT Type",
    "Closed-end Fund/Trust Flag",
    "Fund or Trust Issue Flag",
    "Limited Partnership Flag (Y/N)",
    "Private Placement Flag",
    "Spinoff (Equity Carveout) Type (Code)",
    "Lockup: Lockup Provision Flag",
    "Number of Lockup Days"
]

try:
    input_filepath = config.get_latest_file(config.COUNTRY_INTEGRATION_FILE_PREFIX)
    logging.info(f"Reading: {input_filepath}")
    
    df = pd.read_excel(input_filepath)
    
    # Check for missing columns to avoid KeyError, keep existing ones in the target order
    existing_target_columns = [column for column in target_columns if column in df.columns]
    
    missing_columns = set(target_columns) - set(existing_target_columns)
    if missing_columns:
        logging.warning(f"Following target columns are missing in the input file and will be skipped: {missing_columns}")
        
    # Filter and reorder
    df = df[existing_target_columns]
    logging.info(f"Filtered and reordered down to {len(existing_target_columns)} columns.")
    
    # Save the processed file using config output format
    record_count = len(df)
    output_prefix = f"{config.COUNTRY_INTEGRATION_FILE_PREFIX}_reordered"
    output_filepath = config.get_output_path(output_prefix, record_count)
    
    logging.info(f"Saving processed data to {output_filepath}")
    df.to_excel(output_filepath, index=False)
    logging.info("--- Column filtering and reordering completed ---")
    
except Exception as error:
    logging.error(f"Process failed: {error}")
