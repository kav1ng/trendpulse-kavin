import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "processed_data.csv"


def load_data():
    """Load processed data."""

    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Loaded {len(df)} records.")
        return df

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        print("Run task2_data_processing.py first.")
        return None


def prepare_data(df):
    """Prepare numerical data for visualization."""

    df["score"] = pd.to_numeric(
        df["score"], errors="coerce"
    ).fillna(0)

    df["comments"] = pd.to_numeric(
        df["comments"], errors="coerce"
    ).fillna(0)

    # Shorten long titles for charts
    df["short_title"] = df["title"].apply(
        lambda title: (
            title[:45] + "..."
            if len(str(title)) > 45
            else str(title)
        )
    )

    return df


def create_score_chart(df):
    """Create top stories by score chart."""

    top_10 = df.sort_values(
        by="score",
        ascending=False
    ).head(10)

    chart_data = top_10.sort_values(
        by="score"
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        chart_data["short_title"],
        chart_data["score"]
    )

    plt.xlabel("Score")
    plt.ylabel("Story")
    plt.title("Top 10 Trending Stories by Score")

    plt.tight_layout()

    plt.savefig(
        "top_trending_stories.png",
        dpi=300
    )

    plt.show()

    print("Saved: top_trending_stories.png")


def create_comments_chart(df):
    """Create top stories by comments chart."""

    top_10 = df.sort_values(
        by="comments",
        ascending=False
    ).head(10)

    chart_data = top_10.sort_values(
        by="comments"
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        chart_data["short_title"],
        chart_data["comments"]
    )

    plt.xlabel("Number of Comments")
    plt.ylabel("Story")
    plt.title("Top 10 Stories by Comments")

    plt.tight_layout()

    plt.savefig(
        "top_commented_stories.png",
        dpi=300
    )

    plt.show()

    print("Saved: top_commented_stories.png")


def create_scatter_chart(df):
    """Create score vs comments scatter plot."""

    plt.figure(figsize=(8, 6))

    plt.scatter(
        df["score"],
        df["comments"],
        alpha=0.7
    )

    plt.xlabel("Score")
    plt.ylabel("Comments")
    plt.title("Score vs. Comments")

    plt.tight_layout()

    plt.savefig(
        "score_vs_comments.png",
        dpi=300
    )

    plt.show()

    print("Saved: score_vs_comments.png")


def main():
    print("Starting TrendPulse visualization...")

    df = load_data()

    if df is None:
        return

    df = prepare_data(df)

    print("\nCreating visualizations...")

    create_score_chart(df)

    create_comments_chart(df)

    create_scatter_chart(df)

    print("\nVisualization completed successfully!")


if __name__ == "__main__":
    main()