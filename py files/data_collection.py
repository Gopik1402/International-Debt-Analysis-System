import pandas as pd

# 1 .CSV LOAD
file_name = 'CSV Files/IDS_ALLCountries_Data.csv'
print(f"Loading {file_name}...")
df = pd.read_csv(file_name)

# 2. Understand the structure, columns, and data types
print("\n--- STEP 1: INITIAL INSPECTION ---")

# first 5 rows 
print("\nFirst 5 records:")
print(df.head())

# what data type each column is
print("\nDataFrame Info (Structure & Data Types):")
df.info()

# missing values
print("\nMissing values per column:")
print(df.isnull().sum())