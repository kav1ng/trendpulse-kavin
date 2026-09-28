import pandas as pd


INPUT_FILE = "processed_data.csv"
OUTPUT_FILE = "analysis_results.csv"


def load_data():
    """Load the processed data."""

    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Loaded {len(df)} records.")
        return df

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        print("Run task2_data_processing.py first.")
        return None


def analyze_data(df):
    """Perform trend analysis."""

    # Make sure numerical columns are numeric
    df["score"] = pd.to_numeric(
        df["score"], errors="coerce"
    ).fillna(0)

    df["comments"] = pd.to_numeric(
        df["comments"], errors="coerce"
    ).fillna(0)

    df["engagement"] = pd.to_numeric(
        df["engagement"], errors="coerce"
    ).fillna(0)

    # Calculate overall statistics
    total_stories = len(df)
    average_score = df["score"].mean()
    average_comments = df["comments"].mean()
    average_engagement = df["engagement"].mean()

    # Find the highest scoring story
    top_story = df.loc[df["score"].idxmax()]

    # Find the most commented story
    most_commented = df.loc[df["comments"].idxmax()]

    # Find the highest engagement story
    highest_engagement = df.loc[
        df["engagement"].idxmax()
    ]

    # Get top 10 trending stories
    top_10 = df.sort_values(
        by="score",
        ascending=False
    ).head(10)

    return {
        "total_stories": total_stories,
        "average_score": average_score,
        "average_comments": average_comments,
        "average_engagement": average_engagement,
        "top_story": top_story,
        "most_commented": most_commented,
        "highest_engagement": highest_engagement,
        "top_10": top_10
    }


def save_results(results):
    """Save the top trending stories."""

    top_10 = results["top_10"]

    output = top_10[
        [
            "title",
            "author",
            "score",
            "comments",
            "engagement",
            "url"
        ]
    ]

    output.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nAnalysis results saved to: {OUTPUT_FILE}")


def display_results(results):
    """Display analysis results."""

    print("\n" + "=" * 50)
    print("TRENDPULSE ANALYSIS")
    print("=" * 50)

    print(
        f"\nTotal stories: "
        f"{results['total_stories']}"
    )

    print(
        f"Average score: "
        f"{results['average_score']:.2f}"
    )

    print(
        f"Average comments: "
        f"{results['average_comments']:.2f}"
    )

    print(
        f"Average engagement: "
        f"{results['average_engagement']:.2f}"
    )

    print("\nTop trending story:")
    print(results["top_story"]["title"])

    print(
        f"Score: "
        f"{results['top_story']['score']}"
    )

    print("\nMost commented story:")
    print(results["most_commented"]["title"])

    print(
        f"Comments: "
        f"{results['most_commented']['comments']}"
    )

    print("\nHighest engagement story:")
    print(results["highest_engagement"]["title"])

    print(
        f"Engagement: "
        f"{results['highest_engagement']['engagement']}"
    )

    print("\nTop 10 trending stories:")
    print(
        results["top_10"][
            ["title", "score", "comments", "engagement"]
        ].to_string(index=False)
    )


def main():
    print("Starting TrendPulse analysis...")

    df = load_data()

    if df is None:
        return

    results = analyze_data(df)

    display_results(results)

    save_results(results)

    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()