import re
from email.message import Message

class Mail:
    def __init__(self, body: str, subject: str, sender: str):
        self.body = body
        self.subject = subject
        self.sender = sender

def opt_header_to_str(message: Message, header) -> str:
    results = message.get_all(header)
    return str(results[0]) if results else ''

def unwrap_payload(message: Message) -> str:
    if message.is_multipart():
        parts = message.get_payload()
        return "\n\n".join(unwrap_payload(part) for part in parts)
    else:
        payload = message.get_payload(decode=True)
        if isinstance(payload, bytes):
            payload = payload.decode(errors='replace')
        return payload

def message_to_mail(message: Message) -> Mail:
    body = unwrap_payload(message)
    subject = opt_header_to_str(message, 'Subject')
    sender = opt_header_to_str(message, 'From')
    return Mail(body, subject, sender)

def extract_urls(text):
    return re.findall(r'https?://[^\s)>\]]+', text)

def expand_url(url):
    import requests
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return url
