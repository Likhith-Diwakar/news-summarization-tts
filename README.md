# **News Summarization and Text-to-Speech (TTS) System**

## **Project Overview**
This project extracts key details from news articles related to a company, performs sentiment analysis, and generates a Hindi Text-to-Speech (TTS) output. It leverages **BeautifulSoup** for web scraping, **machine learning models** for sentiment analysis, and an **open-source TTS engine** for audio narration. The **Streamlit** framework is used for the user interface, and the application is deployed on **Hugging Face Spaces**.

---
## 1. News Summarization Model  
**Purpose:** Extracts essential information from lengthy news articles.  

### Models/Methods Used:  
- **Hugging Face Transformers (Abstractive Summarization)**  
  - Likely using `facebook/bart-large-cnn` or `t5-small` to generate summaries in a human-like way.  
- **Sumy (Extractive Summarization)**  
  - Uses algorithms like LexRank and Luhn to select key sentences from the article.  
- **NLTK (Text Processing)**  
  - Helps in tokenizing, sentence segmentation, and filtering unnecessary parts of the news articles.  

---

## 2. Sentiment Analysis Model  
**Purpose:** Determines if the news article has a positive, negative, or neutral sentiment.  

### Models/Methods Used:  
- **Hugging Face Transformers**  
  - Likely using a model like `nlptown/bert-base-multilingual-uncased-sentiment` or `distilbert-base-uncased-finetuned-sst-2-english`.  
- **NLTK’s VADER (Valence Aware Dictionary and sEntiment Reasoner)**  
  - Good for analyzing short texts and headlines.  

---

## 3. Text-to-Speech (TTS) Model  
**Purpose:** Converts the summarized news into Hindi speech.  

### Models/Methods Used:  
- **Google Text-to-Speech (gTTS)**  
  - An easy-to-use API for generating Hindi audio.  
- **Pyttsx3 (Optional)**  
  - If offline TTS is needed, `pyttsx3` can be used.  

## **Key Features**

### **1. News Summarization**
- Uses **Natural Language Processing (NLP)** techniques to extract essential information from lengthy news articles while filtering out unnecessary details.

### **2. Sentiment Analysis**
- Utilizes **machine learning models** to classify the sentiment of news articles as **positive, negative, or neutral**, offering insights into the overall tone and bias of the content.

### **3. Text-to-Speech (TTS)**
- Converts the summarized text into speech using an **open-source TTS engine**, enabling users to listen to news summaries in Hindi.

---

## **Required Python Packages**

To implement this functionality, the following Python libraries are required:

```bash
pip install streamlit newspaper3k transformers torch gTTS pydub requests beautifulsoup4 nltk
```

| **Library**         | **Purpose**                                         |
|--------------------|-------------------------------------------------|
| **streamlit**      | For building the interactive web interface      |
| **newspaper3k**    | Extracting and parsing news articles           |
| **transformers**   | Pre-trained NLP models for summarization       |
| **torch**          | Required for deep learning model operations     |
| **gTTS**          | Google Text-to-Speech API for TTS conversion    |
| **pydub**         | For audio processing tasks                      |
| **requests**      | Handling HTTP requests and API interactions     |
| **beautifulsoup4** | Web scraping and parsing HTML/XML content      |
| **nltk**          | Natural Language Toolkit for text processing    |

---

## **Setting Up the Environment on Ubuntu**

Follow these steps to install dependencies and set up the project:

### **1. Update the Package List**
```bash
sudo apt update
```

### **2. Install Python 3 and Pip**
```bash
sudo apt install python3 python3-pip
```

### **3. Install System Dependencies**
```bash
sudo apt install ffmpeg libsm6 libxext6
```
> These libraries are required for multimedia processing.

### **4. Install Required Python Packages**
```bash
pip3 install streamlit newspaper3k transformers torch gTTS pydub requests beautifulsoup4 nltk
```

---

## **Project Structure**

```
📂 news-summarization-tts
├── app.py                 # Main Streamlit web application
├── summarization.py        # News article extraction & summarization
├── sentiment_analysis.py   # Sentiment analysis module
├── text_to_speech.py       # Text-to-Speech conversion
├── api.py                  # API endpoints for external requests
└── README.md               # Project documentation
```

---

## **Running the Application**

### **1. Testing Sentiment Analysis and TTS Modules Individually**
To test the sentiment analysis and TTS modules separately, run:
```bash
python sentiment_analysis.py
python text_to_speech.py
```

### **2. Running the API Server**
Start the **FastAPI** server using **Uvicorn**:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```plaintext
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7080] using StatReload
INFO:     Started server process [7082]
INFO:     Application startup complete.
```

### **3. Testing API Endpoints Using Curl**
To verify API functionality via terminal:
```bash
curl "http://0.0.0.0:8000/analyze/Google"
```

### **4. Running the Streamlit Web App**
Open a **new terminal** and execute:
```bash
streamlit run app.py
```

**Expected Output:**
```plaintext
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.157.85:8501
```
Visit the local URL to access the web application in your browser.

---

## **Deployment on Hugging Face Spaces**
The application is deployed on **Hugging Face Spaces** for public access.

### **Steps for Deployment:**
1. Create a **new repository** on Hugging Face Spaces.
2. Upload all project files.
3. Add a `requirements.txt` file with the required dependencies.
4. Set up the **Space environment** to run a Streamlit application.
5. Click **Deploy** and wait for the app to go live.

---
### How to Access the API  
1. Start the API server using Uvicorn:  
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
Access the server at:

http://0.0.0.0:8000

# API Endpoints
1. Summarization Endpoint
Endpoint:

[http](http://0.0.0.0:8000)
GET /summarize/{company_name}
Description: Fetches and summarizes news articles related to the specified company.

Example Request:

curl "http://0.0.0.0:8000/summarize/Google"

Response Format:


{
  "company": "Google",
  "summary": "Google has announced new AI features...",
  "source": "https://example.com/news/google"
}


# 2. Sentiment Analysis Endpoint
Endpoint:


GET /analyze/{company_name}
Description: Analyzes the sentiment of summarized news articles.

Example Request:

curl "http://0.0.0.0:8000/analyze/Google"


Response Format:

{
  "company": "Google",
  "sentiment": "Positive",
  "confidence": 0.85
}


# 3. Text-to-Speech (TTS) Endpoint
Endpoint:


GET /tts/{company_name}
Description: Converts the summarized news into Hindi speech and returns the audio file.

Example Request:


curl "http://0.0.0.0:8000/tts/Google" -o google_news.mp3
Response: MP3 file containing the spoken news summary.

API Usage (Third-Party APIs)
The project integrates the following third-party APIs:

Google Text-to-Speech (gTTS):

Converts summarized text to Hindi speech and saves it as an MP3 file.

Newspaper3k:

Extracts and cleans text from online news articles.

Hugging Face Transformers:

Provides pre-trained models for summarization and sentiment analysis.

### **Steps to Contribute:**
1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/news-summarization-tts.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
4. Make changes and commit:
   ```bash
   git commit -m "Add new feature"
   ```
5. Push to your branch and create a pull request:
   ```bash
   git push origin feature-name
   ```

---

## Assumptions & Limitations

### Assumptions
- The news articles fetched using **Newspaper3k** are relevant to the provided company name.
- The **summarization model** effectively captures the key points of an article without distorting the context.
- **Sentiment analysis** is assumed to be accurate for general news articles but may not handle sarcasm or subtle biases well.
- The **TTS model (gTTS)** provides clear and understandable Hindi speech output.
- The API assumes a stable internet connection for fetching news articles and using Hugging Face models.

### Limitations
- **Language Support:** The system primarily works with **English news articles**, and Hindi TTS output may have pronunciation inconsistencies.
- **Summarization Accuracy:** Extractive summarization (Sumy) may not always capture the intended meaning, while abstractive models (T5/BART) might generate minor inaccuracies.
- **Sentiment Analysis Bias:** Pre-trained models may have biases depending on the dataset they were trained on.
- **Dependency on External APIs:** Since we use **Newspaper3k**, **Hugging Face**, and **gTTS**, API downtime or rate limits could affect functionality.
- **Processing Time:** The summarization and sentiment analysis models may take **longer** to process large volumes of news articles.


