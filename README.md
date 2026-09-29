## SDC IPO Data Country Integration
This script (`1_country_integrate.py`) automates the consolidation of country-specific Initial Public Offering (IPO) data downloaded from the SDC Platinum database. Because large SDC queries often fail or time out, data is typically downloaded on a country-by-country basis. This tool merges these individual Excel files into a single master dataset for streamlined downstream analysis.

### Features
* **Alphabetical Concatenation:** Automatically reads and vertically merges all country `.xlsx` files in alphabetical order.
* **Overwrite Protection:** Checks if the consolidated output file already exists and prompts for user confirmation before overwriting.
* **Missing Value Imputation:** Automatically detects empty cells across the dataset and fills them with a dot (`.`) to maintain structural consistency for statistical software.
* **Targeted Extraction:** Specifically targets the `Request 3` worksheet and correctly parses data starting from row 3 (header).

## Filter Non-IPO Records
This script (`2-1_filter_IPOs.py`) removes non-IPO transactions by applying the following rules defined in `config.py`, prints the remaining record count after each criteria, and saves the final statistics to `2-1_filter_IPOs.txt`.

**Keep Records Where:**
*   `Original IPO Flag` = True (Excludes secondary and cross-border dual listings)
*   `Main Tranche within Package flag` = True (Excludes multiple tranche transactions)

**Exclude Records Where:**
*   `Blank Check (SPAC) Involvement Y/N:` = True (Excludes shell companies)
*   `Unit Issues: Unit Issue Flag` = True (Excludes unit issues)
*   `Depositary Issue Flag` = True (Excludes depositary receipts)
*   `Closed-end Fund/Trust Flag` = True (Excludes closed-end funds)
*   `Fund or Trust Issue Flag` = True (Excludes funds and trusts)
*   `Limited Partnership Flag (Y/N)` = True (Excludes limited partnerships)
*   `Private Placement Flag` = True (Excludes private placements)

**Exclude Records Based on Specific Values:**
*   `Issuer/Borrower REIT Type` is not empty (Excludes Real Estate Investment Trusts)
*   `Spinoff (Equity Carveout) Type (Code)` = P (Excludes privatizations of public enterprises)
