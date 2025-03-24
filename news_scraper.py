import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sentiment_analysis import analyze_sentiment  
from collections import Counter
import re

def summarize_text(text):
    """Generate a short summary of the given text."""
    if len(text.split()) < 10:
        return text  # Avoid summarizing very short text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # 2-sentence summary
    return " ".join(str(sentence) for sentence in summary) if summary else "Summary not available"

def extract_topics(summary):
    """Extract potential topics using keyword matching."""
    common_topics = {
        "Technology": ["tech", "software", "hardware", "AI", "cloud", "cybersecurity"],
        "Finance": ["finance", "bank", "investment", "stock", "market", "IPO", "fund"],
        "Stock Market": ["stock", "shares", "trading", "NASDAQ", "investors"],
        "Economy": ["economy", "inflation", "GDP", "growth", "recession"],
        "Innovation": ["innovation", "breakthrough", "disruptive", "startup"],
        "Regulations": ["law", "policy", "regulation", "compliance"],
        "AI": ["artificial intelligence", "machine learning", "deep learning"],
        "Cloud Computing": ["cloud", "AWS", "Google Cloud", "Microsoft Azure"],
        "Mergers": ["acquisition", "merger", "buyout"],
        "Acquisitions": ["acquisition", "buyout", "takeover"],
        "Startups": ["startup", "entrepreneur", "venture", "funding"]
    }

    summary = summary.lower()
    detected_topics = [topic for topic, keywords in common_topics.items() if any(k in summary for k in keywords)]
    return detected_topics if detected_topics else ["Miscellaneous"]  # Fallback if no match

def fetch_news(company):
    """Fetch latest news for the given company from Bing News."""
    query = f"{company} news"
    url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Failed to retrieve news articles. Status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    news_cards = soup.find_all("div", class_="news-card") or soup.find_all("div", class_="newscard")

    for item in news_cards[:10]:
        title_tag = item.find("a", {"class": "title"}) or item.find("h3") or item.find("a", href=True)
        title = title_tag.get_text(strip=True) if title_tag else "No Title Available"
        link = title_tag["href"] if title_tag and "href" in title_tag.attrs else "Link Not Found"
        link = f"https://www.bing.com{link}" if not link.startswith("http") else link
        desc_tag = item.find("div", class_="snippet") or item.find("p")
        description = desc_tag.get_text(strip=True) if desc_tag else title

        summary = summarize_text(description)
        sentiment = analyze_sentiment(description)  #  Uses fixed sentiment function
        topics = extract_topics(description)

        articles.append({"Title": title, "Summary": summary, "Sentiment": sentiment, "Topics": topics, "Link": link})

    return articles
