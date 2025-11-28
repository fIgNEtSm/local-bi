import pandas as pd
# from topic_model import extract_topics
pd.set_option('display.max_columns', None)


reviews = pd.read_csv("dummy_reviews.csv")
reviews["review_date"] = pd.to_datetime(reviews["review_date"])

def create_topic_sentiment_table(reviews):
    data = pd.DataFrame(columns=["date", "topic", "sentiment"])

    for index, row in reviews.iterrows():
        review = row["text"]
        topics = extract_topics(review)
        for topic in topics:
            row_data = {"date": row["review_date"], "topic": topic, "sentiment": topics[topic]}
            data.loc[len(data)] = row_data

    return data

data = pd.read_csv("trends.csv")
data["date"] = pd.to_datetime(data["date"])

data["week"] = data["date"].dt.to_period("W")

weekly_trends = (
    data.groupby(["week", "topic", "sentiment"])
    .size()
    .reset_index(name="count")
)

data["month"] = data["date"].dt.to_period("M")

monthly_trends = (
    data.groupby(["month", "topic", "sentiment"])
    .size()
    .reset_index(name="count")
)

top_monthly_praises = (
    monthly_trends[monthly_trends["sentiment"] == "positive"]
    .sort_values("count", ascending=False)
)

top_monthly_complaints = (
    monthly_trends[monthly_trends["sentiment"] == "negative"]
    .sort_values("count", ascending=False)
)

complaints = weekly_trends[weekly_trends["sentiment"] == "negative"]

complaints_sorted = complaints.sort_values(by=["topic", "week"])

complaints_sorted["previous_count"] = (
    complaints_sorted.groupby("topic")["count"].shift(1)
)

complaints_sorted["change"] = (
        complaints_sorted["count"] - complaints_sorted["previous_count"]
)

spikes = complaints_sorted[complaints_sorted["change"] >= 1]



