import pandas as pd
import os

file_path = r'C:\Users\Welcome\Documents\Projects\International Debt Analysis\CSV Files\IDS_ALLCountries_Data.csv'

print(f"Loading data from:\n{file_path}\n...")

try:
    # 1.CSV Load
    df = pd.read_csv(file_path, encoding='latin1')

    # 2.Drop if Country Name is missing 
    df = df.dropna(subset=['Country Name'])

    # 3.Remove duplicate 
    df = df.drop_duplicates()

    # 4. Drop 2025-2032
    columns_to_drop = [str(year) for year in range(2025, 2033)]
    df = df.drop(columns=columns_to_drop)

    # 5.Coloums to rows
    id_vars = [
        'Country Name', 'Country Code', 'Counterpart-Area Name', 
        'Counterpart-Area Code', 'Series Name', 'Series Code'
    ]

    print("Melting the dataset into long format (this might take a few seconds)...")
    df_melted = df.melt(id_vars=id_vars, var_name='Year', value_name='Debt_Value')

    # 6. Drop if no debt value 
    df_cleaned = df_melted.dropna(subset=['Debt_Value'])

    # 7.Save fn
    output_dir = r'C:\Users\Welcome\Documents\Projects\International Debt Analysis'
    cleaned_file_path = os.path.join(output_dir, 'Cleaned_Debt_Data.csv')
    df_cleaned.to_csv(cleaned_file_path, index=False)

    print("\n--- DATA CLEANING COMPLETE ---")
    print(f"Cleaned dataset saved at: {cleaned_file_path}")
    print(f"Total rows ready for analysis: {len(df_cleaned)}")
    print("\nFirst 5 rows of our new, database-ready format:")
    print(df_cleaned.head())

except FileNotFoundError:
    print("\n ERROR: File not found!")
    print(f"I looked here: {file_path}")
    print("Double check that the file name is spelled exactly like that inside your CSV Files folder!")