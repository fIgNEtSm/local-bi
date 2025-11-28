from keybert import KeyBERT
from sentiment_model import extract_sentiment
import re
from collections import defaultdict

kw_model = KeyBERT(model="all-mpnet-base-v2")


def extract_keywords(review: str):
    keywords = kw_model.extract_keywords(
        review,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=5
    )

    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords


def split_into_opinions(review):
    review = review.lower()
    parts = re.split(r"but|and|however|although|,|\.", review)
    return [p.strip() for p in parts if len(p.strip()) > 3]


def extract_summary(reviews):
    top_complaints = defaultdict(int)
    top_praises = defaultdict(int)

    for review in reviews:
        opinions = split_into_opinions(review)
        for opinion in opinions:
            aspect = extract_keywords(opinion)[0][0]
            sentiment = extract_sentiment(opinion)

            if not aspect:
                continue

            if sentiment == "positive":
                top_praises[aspect] += 1
            elif sentiment == "negative":
                top_complaints[aspect] += 1

    return {"top_praises": top_praises, "top_complains": top_complaints}
