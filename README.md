#News Summarization and Text-to-Speech (TTS) System
This project extracts key details from news articles related to a company, performs sentiment analysis, and generates a Hindi Text-to-Speech (TTS) output. It leverages BeautifulSoup for web scraping, machine learning models for sentiment analysis, and an open-source TTS engine for audio narration. The Streamlit framework is used for the user interface, and the application is deployed on Hugging Face Spaces.

Project Overview
This system automates the process of news consumption by retrieving relevant articles, summarizing their content, analyzing their sentiment, and converting the information into Hindi speech. The user provides a company name, and the system processes the relevant news articles to enhance accessibility and engagement.

Key Features
News Summarization

Uses Natural Language Processing (NLP) techniques to extract essential information from lengthy news articles while filtering out unnecessary details.

Sentiment Analysis

Utilizes machine learning models to classify the sentiment of news articles as positive, negative, or neutral, offering insights into the overall tone and bias of the content.

Text-to-Speech (TTS)

Converts the summarized text into speech using an open-source TTS engine, enabling users to listen to news summaries in Hindi.

Required Python Packages
To implement this functionality, the following Python libraries are required:

streamlit – For building the interactive web interface

newspaper3k – For extracting and parsing news articles

transformers – Provides pre-trained NLP models for summarization and sentiment analysis

torch – Required for deep learning model operations

gTTS – Google Text-to-Speech API for converting text to speech

pydub – For audio processing tasks such as format conversion

requests – For handling HTTP requests and API interactions

beautifulsoup4 – For web scraping and parsing HTML/XML content

nltk – Natural Language Toolkit for text processing

Setting Up the Environment on Ubuntu
Follow these steps to install dependencies and set up the project:

1. Update the Package List
bash
Copy
Edit
sudo apt update
2. Install Python 3 and Pip
bash
Copy
Edit
sudo apt install python3 python3-pip
3. Install System Dependencies
bash
Copy
Edit
sudo apt install ffmpeg libsm6 libxext6
These libraries are required for multimedia processing.

4. Install Required Python Packages
bash
Copy
Edit
pip3 install streamlit newspaper3k transformers torch gTTS pydub requests beautifulsoup4 nltk
Project Structure
The project consists of the following Python files:

app.py – The main script that runs the Streamlit web application and handles user interactions.

summarization.py – Contains functions for extracting and summarizing news articles.

sentiment_analysis.py – Implements sentiment analysis on the summarized text.

text_to_speech.py – Converts text summaries into Hindi speech.

api.py – Manages API endpoints for handling external requests.

Creating the Python Files
Use the following command to create each file using the nano text editor:

bash
Copy
Edit
nano app.py
Repeat this step for each of the files and add the respective code from the GitHub repository.

Running the Application
1. Testing Sentiment Analysis and TTS Modules Individually
To test the sentiment analysis and TTS modules separately, use:

bash
Copy
Edit
python sentiment_analysis.py
python text_to_speech.py
2. Running the API Server
Start the FastAPI server using Uvicorn:

bash
Copy
Edit
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
Expected Output:

plaintext
Copy
Edit
INFO:     Will watch for changes in these directories: ['/home/username/news_summarization/news-summarization-tts']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7080] using StatReload
INFO:     Started server process [7082]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
3. Testing API Endpoints Using Curl
To verify API functionality via terminal:

bash
Copy
Edit
curl "http://0.0.0.0:8000/analyze/Google"
4. Running the Streamlit Web App
Open a new terminal and execute:

bash
Copy
Edit
streamlit run app.py
Expected Output:

plaintext
Copy
Edit
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.157.85:8501
Visit the local URL to access the web application in your browser.

