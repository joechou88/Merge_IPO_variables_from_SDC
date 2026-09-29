import pandas as pd
import config

input_file = config.get_latest_file(config.COUNTRY_INTEGRATION_FILE_PREFIX)
df = pd.read_excel(input_file)

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

final_record_count = len(df)
output_path = config.get_output_path(config.FILTERED_FILE_PREFIX, final_record_count)
df.to_excel(output_path, index=False)

with open("2-1_filter_IPOs.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(filter_statistics))

print(f"\nIPO filtering completed successfully. Total records: {final_record_count}")
print(f"Saved to: {output_path}")
