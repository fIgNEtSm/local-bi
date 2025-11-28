import json
from keyword_extractor import split_into_opinions
from sentiment_model import extract_sentiment
from keybert import KeyBERT


with open("topic_map.json", "r") as file:
    TOPIC_MAP = json.load(file)

# ugh I made a new function cause of keyphrase_ngram_range being (1, 1) instead of using the one in keyword_extractor.py
kw_model = KeyBERT(model="all-mpnet-base-v2")

def extract_keywords(review: str):
    keywords = kw_model.extract_keywords(
        review,
        keyphrase_ngram_range=(1, 1),
        stop_words="english",
        top_n=5
    )
    return keywords[0][0] if keywords else None

def map_topic(word):
    for topic, keywords in TOPIC_MAP.items():
        if word in keywords:
            return topic
    return None

def extract_topics(review):
    result = {}

    opinions = split_into_opinions(review)

    for op in opinions:
        keyword = extract_keywords(op)
        sentiment = extract_sentiment(op)

        if keyword is None:
            continue

        topic = map_topic(keyword)

        if topic:
            result[topic] = sentiment

    return result