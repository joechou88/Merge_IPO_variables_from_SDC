import pandas as pd
import config

df = pd.read_excel(config.COUNTRY_INTEGRATION_PATH)

true_values = [True, 'True', 'TRUE', 'Yes', 'YES', 'Y', 'y', '1', 1]
empty_values = ['.', '']

filter_statistics = []
current_record_count = len(df)

initial_message = f"Initial records: {current_record_count}"
print(initial_message)
filter_statistics.append(initial_message)

for column in config.IPO_FILTER_CRITERIA['keep_true']:
    df = df[df[column].isin(true_values)]
    new_record_count = len(df)
    log_message = f"Keep true for '{column}': {current_record_count} -> {new_record_count}"
    print(log_message)
    filter_statistics.append(log_message)
    current_record_count = new_record_count

for column in config.IPO_FILTER_CRITERIA['exclude_true']:
    df = df[~df[column].isin(true_values)]
    new_record_count = len(df)
    log_message = f"Exclude true for '{column}': {current_record_count} -> {new_record_count}"
    print(log_message)
    filter_statistics.append(log_message)
    current_record_count = new_record_count

for column in config.IPO_FILTER_CRITERIA['exclude_not_empty']:
    df = df[df[column].isin(empty_values) | df[column].isna()]
    new_record_count = len(df)
    log_message = f"Exclude not empty for '{column}': {current_record_count} -> {new_record_count}"
    print(log_message)
    filter_statistics.append(log_message)
    current_record_count = new_record_count

for column, value_to_exclude in config.IPO_FILTER_CRITERIA['exclude_specific_value'].items():
    df = df[df[column] != value_to_exclude]
    new_record_count = len(df)
    log_message = f"Exclude value '{value_to_exclude}' for '{column}': {current_record_count} -> {new_record_count}"
    print(log_message)
    filter_statistics.append(log_message)
    current_record_count = new_record_count

df.to_excel(config.FILTERED_IPO_PATH, index=False)

with open("2-1_filter_IPOs.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(filter_statistics))

print("\nIPO filtering completed successfully.")
