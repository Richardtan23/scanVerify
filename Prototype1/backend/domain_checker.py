# domain_checker.py

import tldextract
import whois
from datetime import datetime

TRUSTED_DOMAINS = {"bbc.com", "reuters.com", "nytimes.com", "cnn.com", "theguardian.com", "npr.org"}
FAKE_DOMAINS = {"abcnews.co.com", "infowars.com", "beforeitsnews.com", "theonion.com", "empirenews.net"}

def get_domain_age_days(domain: str):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        return (datetime.now() - creation_date).days
    except Exception:
        return None

def check_domain_reputation(url: str):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"

    # Step 1: Basic credibility
    if domain in FAKE_DOMAINS:
        credibility = "fake"
        prediction = "fake"
        reason = f"Domain '{domain}' is flagged as fake source"
    elif domain in TRUSTED_DOMAINS:
        credibility = "trusted"
        prediction = "real"
        reason = f"Domain '{domain}' is from a trusted source"
    else:
        credibility = "unknown"
        prediction = None
        reason = "Domain not in known list"

    # Step 2: Age check
    age_days = get_domain_age_days(domain)
    age_status = "old" if age_days and age_days > 180 else "new" if age_days is not None else "unknown"

    return {
        "domain": domain,
        "credibility": credibility,
        "domain_age_days": age_days if age_days is not None else "unknown",
        "age_status": age_status,
        "prediction": prediction,
        "reason": reason
    }
