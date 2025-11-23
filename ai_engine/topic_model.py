from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

labels = ["food", "service", "ambience", "pricing", "staff", "delivery"] # topics

def topic_counts(reviews: list[str], labels: list[str]=labels):
    counts = {label: 0 for label in labels} # dictionary of all the topics/labels with 0 initial value

    
    for review in reviews:
        result = classifier(review, labels)
        top_label = result["labels"][0] # Taking the highest (most relevent) topic for each review
        counts[top_label] += 1 # adding it to the count dictionary

    # returning a json/dict of topics with their counts
    return counts

