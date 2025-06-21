console.log("popup.js loaded");

const analyzeBtn = document.getElementById("analyzeBtn");
const reportBtn = document.getElementById("reportBtn");
const adminBtn = document.getElementById("adminBtn"); 
const resultText = document.getElementById("resultText");
const progressBar = document.getElementById("progressBar");

// Analyze button logic
analyzeBtn.addEventListener("click", async () => {
  resultText.textContent = "Analyzing...";
  progressBar.style.width = "0%";
  progressBar.textContent = "0%";
  progressBar.className = "progress-bar low";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Get visible text from the page
    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.body.innerText
    });

    const pageText = result;
    const pageURL = tab.url;

    // Combine URL and page content for backend analysis
    const response = await fetch("http://localhost:8000/predict/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: `${pageURL}\n${pageText}` })
    });

    const data = await response.json();
    const label = data.prediction.toUpperCase(); // "REAL" or "FAKE"

    let score = label === "REAL" ? 100 : 30;
    let status = label === "REAL"
      ? "✅ High Reliability"
      : "❌ Low Reliability - Likely Fake News";
    let color = label === "REAL" ? "low" : "high";

    progressBar.style.width = `${score}%`;
    progressBar.textContent = `${score}%`;
    progressBar.className = `progress-bar ${color}`;
    resultText.textContent = status;

  } catch (err) {
    console.error("Error analyzing page:", err);
    resultText.textContent = "❗️Analysis failed.";
  }
});


// Report button logic
reportBtn.addEventListener("click", async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const reportedUrl = tab.url;

    // Save to local storage
    chrome.storage.local.get({ reports: [] }, (data) => {
      const newReport = {
        url: reportedUrl,
        date: new Date().toISOString(),
        status: "pending",
        analysis: resultText.textContent // Save current analysis result
      };
      const updatedReports = [...data.reports, newReport];
      
      chrome.storage.local.set({ reports: updatedReports }, () => {
        console.log("Report saved:", newReport);
        resultText.textContent = "✅ Report saved!";

        // Open Google's report page
        const googleUrl = `https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en&url=${encodeURIComponent(reportedUrl)}`;
        chrome.tabs.create({ url: googleUrl });
      });
    });

  } catch (err) {
    console.error("Report failed:", err);
    resultText.textContent = "❗️ Report failed";
  }
});

// Admin button to view reports
adminBtn.addEventListener("click", () => {
  chrome.tabs.create({ url: chrome.runtime.getURL("report.html") });
});