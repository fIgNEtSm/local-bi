from sentiment_model import extract_sentiment
from topic_model import topic_counts
from keyword_extractor import extract_keywords, extract_summary

reviews = [
    "The food was absolutely delicious and full of flavor.",
    "My pasta arrived cold and tasteless.",
    "Portions were huge and the biryani was amazing.",
    "The pizza crust was burnt and the cheese felt cheap.",
    "Service was extremely slow, we waited 40 minutes.",
    "The staff was friendly and checked on us often.",
    "Waiter was rude and ignored our requests.",
    "Quick service and polite employees.",
    "The ambience was cozy with great lighting.",
    "Too noisy and the place felt cramped.",
    "Loved the music and the clean interior.",
    "Tables were dirty and the smell was unpleasant.",
    "The food was great but the prices were too high.",
    "Good value for money, affordable and tasty.",
    "Overpriced for the small portions.",
    "Delivery was fast and the packaging was neat.",
    "My order was messed up and half the items were missing.",
    "Overall a great experience, will come again.",
    "Average food, nothing special.",
    "One of the best restaurants in town!"
]

topics = topic_counts(reviews)

sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}

for review in reviews:
    sentiment_counts[extract_sentiment(review)] += 1


keywords = extract_keywords(reviews)

summary = extract_summary(keywords=keywords)

print(f"Topics: {topics}")
print()
print(f"sentiments: {sentiment_counts}")
print()

print(f"Keywords: {keywords}")
print()

print(f"Summary: {summary}")
