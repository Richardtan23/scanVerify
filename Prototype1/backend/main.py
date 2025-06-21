import uvicorn
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from lr_model import predict_text
from domain_checker import check_domain_reputation
from urllib.parse import urlparse


# Initialize app
app = FastAPI()

# CORS settings (so browser extensions or JS can call the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- You can restrict this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class RequestData(BaseModel):
    text: str

# Root path to show server is running
@app.get("/")
def read_root():
    return {"message": "Fake News Detection API is running."}

# Prediction endpoint
@app.post("/predict/")
async def predict(data: RequestData):
    try:
        # Step 1: Extract domain from any URL in the text
        urls = re.findall(r'https?://[^\s]+', data.text)
        domain = None

        if urls:
            parsed = urlparse(urls[0])  # Take the first URL found
            domain = parsed.netloc

        # Step 2: Domain-based check
        if domain:
            rep = check_domain_reputation(domain)
            if rep["credibility"] == "fake":
                return {
                    "prediction": "fake",
                    "reason": f"Domain '{rep['domain']}' is flagged as suspicious"
                }
            elif rep["credibility"] == "trusted":
                return {
                    "prediction": "real",
                    "reason": f"Domain '{rep['domain']}' is trusted"
                }

        # Step 3: Fall back to text-based prediction
        result = predict_text(data.text)
        return {
            "prediction": result,
            "reason": "Based on text analysis"
        }

    except Exception as e:
        return {
            "error": str(e),
            "prediction": "unknown"
        }

# Run app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)