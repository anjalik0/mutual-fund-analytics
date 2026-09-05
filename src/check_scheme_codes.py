import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(
    fund_master["amfi_code"]
    .dropna()
    .astype(str)
)

nav_codes = set(
    nav_history["amfi_code"]
    .dropna()
    .astype(str)
)

missing_codes = master_codes - nav_codes

print("Total fund master codes:", len(master_codes))
print("Total NAV history codes:", len(nav_codes))

print("\nMissing AMFI codes:")
print(missing_codes)

print("\nNumber of missing codes:", len(missing_codes))