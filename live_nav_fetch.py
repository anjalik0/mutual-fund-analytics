import requests
import pandas as pd
from pathlib import Path


FUNDS = {
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_large_cap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}


OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_fund_nav(fund_name, scheme_code):

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nFetching {fund_name}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = response.json()

    metadata = result["meta"]

    print("Fund:", metadata["scheme_name"])
    print("Scheme Code:", metadata["scheme_code"])
    print("Fund House:", metadata["fund_house"])
    print("Category:", metadata["scheme_category"])

    nav_df = pd.DataFrame(result["data"])

    nav_df["scheme_code"] = scheme_code
    nav_df["fund_name"] = metadata["scheme_name"]

    output_file = OUTPUT_DIR / f"{fund_name}_nav.csv"

    nav_df.to_csv(output_file, index=False)

    print(f"Saved {len(nav_df)} records")
    print(f"File: {output_file}")


def main():

    for fund_name, scheme_code in FUNDS.items():

        try:
            fetch_fund_nav(fund_name, scheme_code)

        except Exception as e:
            print(f"ERROR: {fund_name} -> {e}")


if __name__ == "__main__":
    main()