import re
from urllib.parse import urlparse

def is_phishing_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if "paypal" in domain and not domain.endswith("paypal.com"):
        return True
    if domain.endswith(".ru") or domain.endswith(".cn"):
        return True
    if re.search(r'\d{1,3}(\.\d{1,3}){3}', domain):
        return True
    return False

def annotate_phishing_urls(body: str, phishing_urls: list) -> str:
    def replace_func(match):
        url = match.group(0)
        if url in phishing_urls:
            return f'[CẢNH BÁO: {url}]'
        return url

    url_pattern = re.compile(r'https?://[^\s]+')
    return re.sub(url_pattern, replace_func, body)
