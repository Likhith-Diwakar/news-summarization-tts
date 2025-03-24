from fastapi import FastAPI
import uvicorn
from news_scraper import fetch_news
from sentiment_analysis import analyze_sentiment
import json

app = FastAPI()

@app.get("/analyze/{company}")
def analyze(company: str):
    # Get articles using your existing fetch_news function
    articles = fetch_news(company)

    # The sentiment should already be included in your fetch_news results,
    # but we can ensure it's properly set here
    for article in articles:
        # Only analyze if not already done by fetch_news
        if 'Sentiment' not in article or not article['Sentiment']:
            article['Sentiment'] = analyze_sentiment(article['Summary'])

    # Calculate sentiment distribution
    sentiment_scores = {
        "Positive": sum(1 for a in articles if a["Sentiment"] == "Positive"),
        "Negative": sum(1 for a in articles if a["Sentiment"] == "Negative"),
        "Neutral": sum(1 for a in articles if a["Sentiment"] == "Neutral")
    }

    comparative_analysis = {"Sentiment Distribution": sentiment_scores}

    report = {
        "Company": company,
        "Articles": articles,
        "Comparative Sentiment Score": comparative_analysis
    }

    # Note: Removed text-to-speech for now as it wasn't in your earlier code
    # If needed, you can add it back once that module is properly implemented

    return report

if __name__ == "__main__":  # Fixed the underscores here
    uvicorn.run(app, host="0.0.0.0", port=8000)
