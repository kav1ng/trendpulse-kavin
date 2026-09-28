import pandas as pd


INPUT_FILE = "raw_data.csv"
OUTPUT_FILE = "processed_data.csv"


def load_data():
    """Load the raw data collected in Task 1."""
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Loaded {len(df)} records from {INPUT_FILE}")
        return df

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        print("Run task1_data_collection.py first.")
        return None


def clean_data(df):
    """Clean and prepare the trending data."""

    # Remove duplicate stories
    df = df.drop_duplicates(subset="id")

    # Remove rows without a title
    df = df.dropna(subset=["title"])

    # Fill missing numerical values
    df["score"] = pd.to_numeric(
        df["score"], errors="coerce"
    ).fillna(0)

    df["comments"] = pd.to_numeric(
        df["comments"], errors="coerce"
    ).fillna(0)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    # Convert collected_at to datetime
    df["collected_at"] = pd.to_datetime(
        df["collected_at"], errors="coerce"
    )

    # Remove rows with invalid timestamps
    df = df.dropna(subset=["timestamp"])

    # Clean text fields
    df["title"] = df["title"].str.strip()

    df["author"] = (
        df["author"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # Clean URLs
    df["url"] = df["url"].fillna("No URL")

    # Create a simple engagement metric
    df["engagement"] = df["score"] + df["comments"]

    # Sort by score
    df = df.sort_values(
        by="score",
        ascending=False
    )

    # Reset index
    df = df.reset_index(drop=True)

    return df


def save_data(df):
    """Save the processed data."""
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nProcessed data saved to: {OUTPUT_FILE}")
    print(f"Final number of records: {len(df)}")


def main():
    print("Starting data processing...")

    df = load_data()

    if df is None:
        return

    print("\nCleaning data...")

    processed_df = clean_data(df)

    save_data(processed_df)

    print("\nProcessed data preview:")
    print(processed_df.head())

    print("\nColumns:")
    print(list(processed_df.columns))


if __name__ == "__main__":
    main()