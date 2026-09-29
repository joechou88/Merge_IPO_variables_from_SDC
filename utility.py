import pandas as pd

def convert_datetime_to_date(df):
    # Date formatting: Convert 'YYYY-MM-DD 00:00:00' datetime format to 'YYYY/M/D' format since pandas automatically appends timestamps when reading Excel serial dates.
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y/%m/%d').str.replace(r'(?<=/)0', '', regex=True)
            
    return df
