import imaplib, email
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
        return "\n\n".join(unwrap_payload(part) for part in message.get_payload())
    payload = message.get_payload(decode=True)
    return payload.decode(errors='replace') if isinstance(payload, bytes) else payload

def message_to_mail(message: Message) -> Mail:
    return Mail(
        body=unwrap_payload(message),
        subject=opt_header_to_str(message, 'Subject'),
        sender=opt_header_to_str(message, 'From')
    )

def connect_and_fetch_emails(imap_url, user, password, sender_filter):
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select("inbox")
    _, data = my_mail.search(None, 'FROM', f'"{sender_filter}"')
    mail_ids = data[0].split()
    messages = []
    for num in mail_ids:
        _, data = my_mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        messages.append(msg)
    return messages
