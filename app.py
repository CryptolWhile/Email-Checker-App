import streamlit as st
import joblib
from utils.email_utils import connect_and_fetch_emails, message_to_mail
from utils.text_preprocessing import preprocess_text
from utils.phishing import detect_phishing_urls

# Load model và vectorizer
model = joblib.load("models/spam_nb_model.joblib")
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")

st.title(" Email Spam & Phishing Detector")

# Lấy thông tin email từ secrets.toml
imap_url = st.secrets["email"]["imap_url"]
user = st.secrets["email"]["user"]
password = st.secrets["email"]["password"]
sender_filter = st.secrets["email"]["sender_filter"]

st.markdown("#### ✅ Đang sử dụng thông tin từ `.streamlit/secrets.toml`")

if st.button("📥 Kết nối & kiểm tra email"):
    with st.spinner("Đang lấy email..."):
        try:
            messages = connect_and_fetch_emails(imap_url, user, password, sender_filter)
            if not messages:
                st.warning("Không tìm thấy email nào.")
            else:
                st.success(f"Đã lấy {len(messages)} email.")
                for i, msg in enumerate(messages[:5]):
                    mail = message_to_mail(msg)
                    clean_text = preprocess_text(mail.body)
                    X_input = vectorizer.transform([clean_text])
                    prediction = model.predict(X_input)[0]
                    prediction_proba = model.predict_proba(X_input)[0]

                    st.subheader(f" Email #{i+1}")
                    st.write(f"**From:** {mail.sender}")
                    st.write(f"**Subject:** {mail.subject}")
                    st.write(f"**Body:** {mail.body[:500]}...")

                    st.write("🔍 **Phishing URL(s):**")
                    urls = detect_phishing_urls(mail.body)
                    if urls:
                        for u in urls:
                            st.error(u)
                    else:
                        st.success("Không phát hiện URL đáng ngờ.")

                    st.write(f" **Spam Prediction:** `{prediction}`")
                    st.progress(prediction_proba[1])  # Assuming 1=spam
        except Exception as e:
            st.error(f"❌ Đã xảy ra lỗi: {e}")
