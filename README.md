# 📫 Email Checker App: Spam & Phishing Detection via IMAP + ML

Detect spam emails and phishing links from your inbox using IMAP, TF-IDF + Naive Bayes, and link analysis — all wrapped in an interactive Streamlit UI.

![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![Top Lang](https://img.shields.io/github/languages/top/CryptolWhile/Email-Checker-App?style=flat-square)
![License](https://img.shields.io/github/license/CryptolWhile/Email-Checker-App?style=flat-square)

---


## 🎯 Overview

This app allows you to:

- 📥 Connect securely to your inbox via IMAP
- 🤖 Detect spam with ML (TF-IDF + Naive Bayes)
- 🕵️ Flag suspicious/phishing URLs
- 💻 Visualize results through a clean Streamlit dashboard

---

## 🧠 Features

✅ IMAP inbox reading  
✅ Customizable spam detection pipeline  
✅ Real-time phishing URL scanner  
✅ Streamlit interface for non-technical users  
✅ Secure secrets management with `secrets.toml`

---

## 🗂️ Project Structure

```

email_checker_app/
├── app.py
├── requirements.txt
├── models/
│   ├── spam_nb_model.joblib
│   └── tfidf_vectorizer.joblib
├── utils/
│   ├── __init__.py
│   ├── email_utils.py
│   ├── text_preprocessing.py
│   └── phishing.py
└── .streamlit/
    ├── config.toml
    └── secrets.toml


````

---

## 🚀 Getting Started

### 📦 Installation

```bash
git clone https://github.com/yourusername/email_checker_app.git
cd email_checker_app
pip install -r requirements.txt
````

### 🔐 Setup Secrets

Create `.streamlit/secrets.toml`:

```toml
[credentials]
imap_url = "imap.gmail.com"
email = "your_email@gmail.com"
password = "your_app_password"
sender_filter = "alerts@bank.com"

[paths]
model_path = "models/spam_nb_model.joblib"
vectorizer_path = "models/tfidf_vectorizer.joblib"
```

> ⚠️ For Gmail, enable IMAP and use an **App Password** (if 2FA enabled).

### ▶️ Run App

```bash
streamlit run app.py
```

---

## 📊 How It Works

| Step       | Function                             |
| ---------- | ------------------------------------ |
| 🔐 Login   | Connect to mailbox via IMAP          |
| 📥 Fetch   | Get emails from specific senders     |
| 🧹 Clean   | Normalize + tokenize text            |
| 🧠 Predict | TF-IDF + Naive Bayes for spam        |
| 🚨 Detect  | Regex + heuristics for phishing URLs |

---

## 💻 UI Preview



---

## 🧪 Example Email Results

| Email Subject             | Spam  | Phishing |
| ------------------------- | ----- | -------- |
| "Verify your account now" | ✅ Yes | ✅ Yes    |
| "Team Standup Notes"      | ❌ No  | ❌ No     |

---


## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.

---

