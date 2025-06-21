// content.js

// 1. Clean, simplified overlay function
function createOverlay(label, reason) {
  const existing = document.getElementById("scanverify-overlay");
  if (existing) existing.remove();

  const overlay = document.createElement("div");
  overlay.id = "scanverify-overlay";
  overlay.style.position = "fixed";
  overlay.style.bottom = "20px";
  overlay.style.right = "20px";
  overlay.style.zIndex = "99999";
  overlay.style.backgroundColor = label === "REAL" ? "#d4edda" : "#f8d7da";
  overlay.style.color = label === "REAL" ? "#155724" : "#721c24";
  overlay.style.border = "1px solid #ccc";
  overlay.style.padding = "16px";
  overlay.style.borderRadius = "8px";
  overlay.style.boxShadow = "0 2px 6px rgba(0, 0, 0, 0.15)";
  overlay.innerHTML = `
    <strong>ScanVerify Result</strong><br>
    <p>Prediction: <strong>${label}</strong></p>
    <p>${reason}</p>
    <button id="close-scanverify-overlay" style="margin-top:10px; padding:4px 8px; cursor:pointer;">Close</button>
  `;

  document.body.appendChild(overlay);
  document.getElementById("close-scanverify-overlay").onclick = () => overlay.remove();
}

// 2. Analyze the article: extract domain and text
const url = window.location.href;
const text = document.body.innerText.slice(0, 1000);

fetch("http://localhost:8000/predict/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: `${text}\n${url}` }) // Include URL in the payload
})
  .then(res => res.json())
  .then(data => {
    const label = data.prediction.toUpperCase(); // "FAKE" or "REAL"
    const reason = data.reason || "Analyzed by AI model";
    createOverlay(label, reason);
  })
  .catch(error => {
    console.error("ScanVerify error:", error);
    createOverlay("UNKNOWN", "Failed to analyze this page.");
  });
