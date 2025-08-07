from textblob import TextBlob

def analyze_feedback(feedback_text):
    """
    Analyze the feedback sentiment and extract tags.
    """
    # Sentiment Analysis
    blob = TextBlob(feedback_text)
    sentiment = "positive" if blob.sentiment.polarity > 0 else "negative" if blob.sentiment.polarity < 0 else "neutral"

    # Very basic tag extraction (split keywords)
    words = [word.lower() for word in feedback_text.split() if len(word) > 3]
    tags = list(set(words[:5]))  # first 5 unique keywords

    return {
        "sentiment": sentiment,
        "tags": tags
    }
