import pandas as pd

# File Paths
data_path = r'C:\Users\Welcome\Documents\Projects\International Debt Analysis\Cleaned_Debt_Data.csv'
metadata_path = r'C:\Users\Welcome\Documents\Projects\International Debt Analysis\CSV Files\IDS_CountryMetaData.csv'

print("Loading cleaned dataset and metadata...")
df = pd.read_csv(data_path)

try:
    meta_df = pd.read_csv(metadata_path, encoding='latin1')
    
    # 1.Delete invisible space
    df['Country Code'] = df['Country Code'].astype(str).str.strip()
    valid_country_codes = meta_df.dropna(subset=['Region'])['Code'].astype(str).str.strip().tolist()
    
    # 2.Valid country codes
    df = df[df['Country Code'].isin(valid_country_codes)]
    print(f"\n Successfully filtered out aggregate groups. Analyzing {df['Country Name'].nunique()} true countries only!")
except FileNotFoundError:
    print("\n Could not find the metadata file. Make sure the path is correct!")

# Total debt 
total_debt_indicator = 'External debt stocks, total (DOD, current US$)'
debt_df = df[df['Series Name'] == total_debt_indicator]

print("     EXPLORATORY DATA ANALYSIS (EDA)    ")

# Countrywise debt
print("1. COUNTRY-WISE DEBT ")
country_totals = debt_df.groupby('Country Name')['Debt_Value'].sum().sort_values(ascending=False)

print("\nTop 5 COUNTRIES with HIGHEST Total Debt (in Billions USD):")
for country, value in country_totals.head(5).items():
    print(f"- {country}: ${value / 1_000_000_000:,.2f} Billion")

print("\nTop 5 COUNTRIES with LOWEST Total Debt :")
lowest_countries = country_totals[country_totals > 0].tail(5)
for country, value in lowest_countries.items():
    print(f"- {country}: ${value / 1_000_000:,.2f} Million")


# Indicators
print("\n 2. DEBT INDICATOR IMPACT ")
print("Top 5 Indicators contributing the most massive financial volumes:")
top_indicators = df.groupby('Series Name')['Debt_Value'].sum().sort_values(ascending=False).head(5)
for indicator, value in top_indicators.items():
    print(f"- {indicator[:50]}... : ${value / 1_000_000_000_000:,.2f} Trillion")


# Trends,pattern & relations
print("\n 3. GLOBAL DEBT TRENDS, PATTERNS & RELATIONSHIPS ")

# Group by year 
yearly_trend = debt_df.groupby('Year')['Debt_Value'].sum().sort_index()

if not yearly_trend.empty:
    # Year-over-Year (YoY) Percentage Growth
    yoy_growth = yearly_trend.pct_change() * 100
    
    # aggressive debt spike
    max_growth_year = yoy_growth.idxmax()
    max_growth_rate = yoy_growth.max()
    
    # Calculate overall growth 
    start_year = yearly_trend.index[0]
    end_year = yearly_trend.index[-1]
    total_growth_pct = ((yearly_trend.iloc[-1] - yearly_trend.iloc[0]) / yearly_trend.iloc[0]) * 100
    
    print(f" Overall Growth: From {start_year} to {end_year}, global external debt grew by a staggering {total_growth_pct:,.1f}%.")
    print(f" Largest Spike: The most aggressive single-year jump was in {max_growth_year}, with debt increasing by {max_growth_rate:,.1f}% compared to the previous year.")
    
    print("\nKey Milestone Years (in Trillions USD):")
    milestone_years = ['2000', '2008', '2015', '2020', '2023']
    for year in milestone_years:
        # Check year is in index or int
        if year in yearly_trend.index or int(year) in yearly_trend.index:
            try:
                val = yearly_trend[year]
            except KeyError:
                val = yearly_trend[int(year)]
            trillions = val / 1_000_000_000_000
            print(f"- Year {year}: ${trillions:,.2f} Trillion")
else:
    print("Not enough data to calculate trends. Double-check the dataset filtering.")

print("               EDA COMPLETELY FINISHED            ")