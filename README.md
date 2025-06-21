# ScanVerify - Chrome Extension for Fake News Detection

**ScanVerify** is a browser extension that helps users detect fake news and misinformation on any webpage. It combines **domain reputation checks** with **AI-powered content analysis** to show how credible an article is — all with a single click.

---

## Key Features

 **Domain Checker**  
- Detects if a webpage comes from a **trusted**, **unknown**, or **suspicious** news source.

 **AI-Powered Text Analysis**  
- Uses **Natural Language Processing (NLP)** and **Machine Learning** to analyze article content.

 **Reliability Score**  
- Shows a percentage-based score indicating how credible the page likely is.

 **Report Suspicious Content**  
- Users can report misleading pages with one click, stored locally for admin review.

---

## How It Works

1. Open any news article in your browser.
2. Click the **ScanVerify** icon in the Chrome toolbar.
3. Click **"Analyze"**.
   - If the website is trusted, you'll get an immediate "Real" result.
   - If not, the extension reads and sends article text to an API for deeper analysis.
4. You'll see a **reliability score**, color-coded (Green = Real, Yellow = Medium, Red = Likely Fake).
5. Optionally, click **"Report"** to save the page info and open Google's official phishing report page.
6. Click gear icon to check the reported Urls.

---

## Tech Stack

### Frontend (Chrome Extension)
- HTML / CSS / JavaScript
- Chrome Extension APIs
- Popup UI (`popup.html`, `popup.js`)
- Content Script (`content.js`)
- Local Storage for reports
- Admin view (`report.html`, `report.js`)

### Backend (FastAPI)
- Python 3, FastAPI
- `uvicorn` server
- Machine Learning (Logistic Regression)
- NLP: TextBlob, TF-IDF vectorizer
- Domain Reputation Checker

---

## Project Structure
ScanVerify/
├── popup.html # Extension popup UI
├── popup.js # Handles Analyze & Report buttons
├── content.js # Analyzes page content + shows overlay
├── report.html # View saved reports
├── report.js # Script for viewing local reports
├── style.css # Styling for popup and overlays
├── manifest.json # Chrome extension settings
├── backend/
│ ├── main.py # FastAPI server
│ ├── domain_checker.py # Checks domain reputation
│ ├── lr_model.py # Predicts text credibility
│ ├── tfidf_vectorizer.pkl # Loaded model file
│ └── logistic_model.pkl # Trained ML model


---

## Getting Started

### Step 1: Setup the Backend API

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn scikit-learn textblob nltk joblib
   
2. Download the trained models:
   logistic_model.pkl
    tfidf_vectorizer.pkl

3. Run the FastAPI server:
   ```bash
    uvicorn main:app --reload
   
### Step 2: Load the Chrome Extension
1. Open Chrome and go to chrome://extensions/

2. Enable Developer Mode (top right).

3. Click Load Unpacked and select the extension folder.

4. You’ll see the ScanVerify icon in your Chrome toolbar.

## Test It Live
Try testing with:

Real article: BBC News
Fake article: NewsPunch, The People's Voice

Click the extension, analyze the page, and see the result!

## Report View
Click the gear icon in the popup to view previously reported pages. Stored using Chrome's local storage.



