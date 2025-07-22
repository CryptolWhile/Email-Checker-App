import re

def detect_phishing_urls(text: str):
    url_pattern = r'https?://[^\s"]+'
    urls = re.findall(url_pattern, text)
    suspicious = []
    for url in urls:
        if any(keyword in url for keyword in ["free", "login", "verify", "click", "secure", "update"]):
            suspicious.append(url)
    return suspicious
