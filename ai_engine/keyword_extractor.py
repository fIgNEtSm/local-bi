from keybert import KeyBERT
from sentiment_model import extract_sentiment

kw_model = KeyBERT(model="all-MiniLM-L6-v2")

def extract_keywords(reviews: list):
    top_keywords = []
    for review in reviews:
        keywords = kw_model.extract_keywords(
            review,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=3
        )
    
        top_keywords += keywords
    top_keywords.sort(key=lambda x:x[1], reverse=True)
    
    return top_keywords

def extract_summary(keywords: list[tuple[str, float]]):
    summary = {
        "top_complains": [],
        "top_praises": [],
        "others": [],
    }

    for keyword, score in keywords:
        keyword_sentiment = extract_sentiment(keyword)
        
        if keyword_sentiment == "positive":
            summary["top_praises"].append(keyword)
        elif keyword_sentiment == "negative":
            summary["top_complains"].append(keyword)
        else:
            summary["others"].append(keyword)
    return summary