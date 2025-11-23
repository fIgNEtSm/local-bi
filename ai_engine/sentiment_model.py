from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def extract_sentiment(review: str):
    score = sia.polarity_scores(review)
    comp = score["compound"]
    if comp > 0.05:
        return "positive"
    elif comp < -0.05:
        return "negative"
    else:
        return "neutral"
  
