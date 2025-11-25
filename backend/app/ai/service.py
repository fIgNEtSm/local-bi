
def perform_ai_analysis(reviews: list[str]):
    """
    reviews: list of review texts
    returns: dictionary containing AI analysis results
    """


    return {
        "sentiment_pos": 12,
        "sentiment_neg": 3,
        "sentiment_neu": 5,
        "top_topics": {"food": 50, "service": 20},
        "keywords": ["biryani", "slow service"],
        "top_complaints": ["slow service"],
        "top_praises": ["food taste"],
        "ai_insights": "Customers like the food but complain about slow service."
    }
