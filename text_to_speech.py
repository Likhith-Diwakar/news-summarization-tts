from gtts import gTTS
import re
from googletrans import Translator  # Importing Translator for translation

def clean_text(text):
    """Removes unnecessary symbols and extra spaces before converting to speech."""
    text = re.sub(r'[{};=,.]', '', text)  # Remove unwanted symbols
    return text.strip()  # Remove leading/trailing spaces

def generate_tts(news_data):
    """Converts structured news data into Hindi speech and saves it as an MP3 file."""

    # Initialize the translator
    translator = Translator()

    text = ""
    for i, article in enumerate(news_data.get("Articles", []), 1):  # Ensure Articles exist, add numbering
        title = clean_text(article.get("Title", "कोई शीर्षक नहीं"))
        summary = clean_text(article.get("Summary", "कोई सारांश उपलब्ध नहीं"))
        sentiment = clean_text(article.get("Sentiment", "अनिश्चित"))
        topics = ", ".join(article.get("Topics", ["कोई विशिष्ट विषय नहीं"]))

        # Construct properly formatted speech text (in English for now)
        text += f"News {i}: \n"
        text += f"Title: {title}.\n"
        text += f"Summary: {summary}.\n"
        text += f"Sentiment: {sentiment}.\n"
        text += f"Topics: {topics}.\n\n"

    # Translate the entire text from English to Hindi
    translated_text = translator.translate(text, src='en', dest='hi').text

    # Convert translated Hindi text to speech
    tts = gTTS(text=translated_text, lang='hi', slow=False)  # Ensure slow=False for normal speed
    tts.save("tts_output.mp3")  # Save as MP3 file

    print("✅ Hindi speech saved as 'tts_output.mp3' successfully!")

# Example Usage (Testing)
if __name__ == "__main__":
    sample_data = {
        "Articles": [
            {
                "Title": "IBM plans to lay off 9,000 employees.",
                "Summary": "IBM has announced significant cuts in its cloud division.",
                "Sentiment": "Negative",
                "Topics": ["Technology", "Cloud Computing"]
            },
            {
                "Title": "IBM added to Wedbush's Best Ideas list.",
                "Summary": "IBM is now listed alongside Apple and Microsoft in Wedbush's list.",
                "Sentiment": "Positive",
                "Topics": ["Finance", "Stock Market"]
            }
        ]
    }
    generate_tts(sample_data)
