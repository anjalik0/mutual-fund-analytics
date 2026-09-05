import pandas as pd
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


def load_csv_files():
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))

    print(f"Found {len(csv_files)} CSV files")

    for file in csv_files:
        print("\n" + "=" * 60)
        print(f"FILE: {file.name}")
        print("=" * 60)

        try:
            df = pd.read_csv(file)

            print("Shape:", df.shape)
            print("\nData Types:")
            print(df.dtypes)

            print("\nFirst 5 Rows:")
            print(df.head())

            print("\nMissing Values:")
            print(df.isnull().sum())

        except Exception as e:
            print(f"Error reading {file.name}: {e}")


if __name__ == "__main__":
    load_csv_files()