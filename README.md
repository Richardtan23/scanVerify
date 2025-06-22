# ScanVerify – Fake News Detection Chrome Extension

*Team:Taste of Fate
*Teams Member:Clive Timothy Haye Ng,Pok Hao Yang,Tan Li Cherk,Boon Keat



**ScanVerify** is a Chrome extension that helps users detect and flag potentially fake news articles. It integrates domain reputation analysis and a machine learning text classifier to determine the credibility of the content displayed in a web browser.

---

## Table of Contents

* [Features](#features)
* [How It Works](#how-it-works)
* [Installation Guide](#installation-guide)
* [Usage](#usage)
* [Backend Setup](#backend-setup)
* [Dependencies](#dependencies)
* [Expected Outcomes](#expected-outcomes)
---

## Features

* Domain reputation analysis using a whitelist/blacklist approach.
* Text-based fake news detection using a logistic regression model.
* Real-time analysis via Chrome extension interface.
* Visual reliability scoring via progress bar and textual feedback.
* Reporting system for users to flag suspicious articles.
* Local storage of reports for review.

---

## How It Works

1. When a user opens a news article and clicks the "Analyze" button:

   * The extension checks the current page URL.
   * If the domain is in a known list (trusted/fake), it returns a quick result.
   * If unknown, the extension sends the article text to a FastAPI backend.
   * The backend uses a trained model to analyze the content and return a prediction.
2. Results are presented in the popup with a reliability score and label (real/fake).

---

## Installation Guide

### Chrome Extension (Frontend)

1. Clone the repository:

   ```
   git clone https://github.com/Richardtan23/scanVerify.git
   ```
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable **Developer mode**
4. Click **Load Unpacked** and select the extension directory

---

## Backend Setup

1. Navigate to the `backend/` folder in the project
2. Install Python dependencies using:

   ```
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:

   ```
   uvicorn main:app --reload
   ```

---

## Usage

* Visit any news article
* Click the Chrome extension icon
* Press "Analyze" to check credibility
* View results in the popup (prediction and reliability score)
* Optionally, press "Report" to flag the page

---

## Dependencies

### requirements.txt

```
fastapi
uvicorn
pydantic
tldextract
python-whois
nltk
textblob
scikit-learn
joblib
```

To install all required packages:

```
pip install -r requirements.txt
```

---

## Expected Outcomes

* Improved user awareness of credible and misleading information sources.
* A tool for early detection of misinformation in browsing sessions.
* An interface for easily reporting and reviewing suspicious news content.

## Checking the reported Urls 
By clicking the gear icon, you to can check the urls that you reported to the google.
