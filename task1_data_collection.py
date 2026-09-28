import requests
import pandas as pd
from datetime import datetime


API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

NUMBER_OF_STORIES = 50


def fetch_story_ids():
    """Fetch IDs of the current top stories."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()[:NUMBER_OF_STORIES]


def fetch_story(story_id):
    """Fetch details for one story."""
    response = requests.get(ITEM_URL.format(story_id), timeout=10)

    if response.status_code != 200:
        return None

    return response.json()


def collect_data():
    story_ids = fetch_story_ids()

    records = []

    for story_id in story_ids:
        story = fetch_story(story_id)

        if story is None:
            continue

        records.append({
            "id": story.get("id"),
            "title": story.get("title"),
            "author": story.get("by"),
            "score": story.get("score", 0),
            "comments": story.get("descendants", 0),
            "url": story.get("url"),
            "timestamp": story.get("time")
        })

    df = pd.DataFrame(records)

    # Convert Unix timestamp to readable datetime
    if not df.empty:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            unit="s",
            errors="coerce"
        )

        df["collected_at"] = datetime.now()

    return df


def main():
    print("Fetching live trending data...")

    df = collect_data()

    if df.empty:
        print("No data was collected.")
        return

    df.to_csv("raw_data.csv", index=False)

    print(f"Successfully collected {len(df)} stories.")
    print("Saved data to: raw_data.csv")

    print("\nSample data:")
    print(df.head())


if __name__ == "__main__":
    main()