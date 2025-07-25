import streamlit as st
import imaplib, email, json
from pathlib import Path
import pandas as pd
from datetime import datetime
import joblib

# Import module riêng
from utils.email_utils import message_to_mail, extract_urls, expand_url
from utils.text_preprocessing import preprocess_text
from utils.phishing import is_phishing_url, annotate_phishing_urls

# ========== Load model ==========
@st.cache_resource
def load_model():
    model = joblib.load(Path("models/spam_nb_model.joblib"))
    vectorizer = joblib.load(Path("models/tfidf_vectorizer.joblib"))
    return model, vectorizer

model, vectorizer = load_model()

# ========== Log ==========
LOG_PATH = Path("logs/email_events.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
if not LOG_PATH.exists():
    LOG_PATH.write_text("[]")

@st.cache_data
def load_logs():
    try:
        return json.loads(LOG_PATH.read_text())
    except:
        return []

def save_logs(logs):
    LOG_PATH.write_text(json.dumps(logs, indent=2))
    load_logs.clear()

def log_event(user, mail, verdict, phishing_links):
    logs = load_logs()
    logs.append({
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "sender": mail.sender,
        "subject": mail.subject,
        "urls": phishing_links,
        "verdict": verdict
    })
    save_logs(logs)

# ========== UI ==========
st.title("📥 Email Checker: Spam + Phishing Detection")

tab1, tab2 = st.tabs(["Kiểm tra Email", "Lịch sử kiểm tra"])

# --- TAB 1: Kiểm tra Email ---
with tab1:
    with st.form("email_form"):
        imap_url = st.text_input("IMAP server", "imap.gmail.com")
        user = st.text_input("Email", "your_email@gmail.com")
        password = st.text_input("Mật khẩu (hoặc App Password)", type="password")
        sender_filter = st.text_input("Lọc người gửi", "example@spam.com")
        submitted = st.form_submit_button("Kết nối và kiểm tra")

    if submitted:
        try:
            mail_client = imaplib.IMAP4_SSL(imap_url)
            mail_client.login(user, password)
            mail_client.select("inbox")
            _, data = mail_client.search(None, 'FROM', f'"{sender_filter}"')
            mail_ids = data[0].split()

            if not mail_ids:
                st.warning("❗ Không tìm thấy email từ người gửi này.")
            else:
                st.success(f"Đã tìm thấy {len(mail_ids)} email. Hiển thị 5 email mới nhất:")

                for num in mail_ids[-5:]:
                    _, data = mail_client.fetch(num, '(RFC822)')
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    mail = message_to_mail(msg)

                    # URL check
                    urls = extract_urls(mail.body)
                    expanded_urls = [expand_url(u) for u in urls]
                    phishing_links = [u for u in expanded_urls if is_phishing_url(u)]
                    annotated_body = annotate_phishing_urls(mail.body, phishing_links)

                    # Spam detection
                    full_text = mail.subject + " " + mail.body
                    input_data = [preprocess_text(full_text)]
                    input_features = vectorizer.transform(input_data)
                    prediction = model.predict(input_features)[0]

                    verdict = "✅ HỢP LỆ" if prediction == 0 and not phishing_links else "❌ NGHI NGỜ"
                    color = "green" if verdict.startswith("✅") else "red"

                    # Log
                    log_event(user, mail, verdict, phishing_links)

                    # Display
                    st.markdown("---")
                    st.markdown(f"**Tiêu đề:** {mail.subject}")
                    st.markdown(f"**Người gửi:** `{mail.sender}`")
                    st.markdown(f"**Kết luận:** <span style='color:{color}'>{verdict}</span>", unsafe_allow_html=True)
                    if phishing_links:
                        st.markdown("⚠️ **Phát hiện các link đáng ngờ:**")
                        for link in phishing_links:
                            st.markdown(f"- {link}")
                    st.text_area("📄 Nội dung", value=annotated_body, height=200)

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")

# --- TAB 2: Lịch sử kiểm tra ---
with tab2:
    logs = load_logs()

    if not logs:
        st.info("Chưa có lịch sử kiểm tra nào.")
    else:
        df_logs = pd.DataFrame(logs)
        df_logs["timestamp"] = pd.to_datetime(df_logs["timestamp"])
        df_logs = df_logs.sort_values("timestamp", ascending=False).head(100)

        st.dataframe(
            df_logs[["timestamp", "user", "sender", "subject", "verdict"]],
            use_container_width=True,
            hide_index=True
        )

        if st.button("🗑 Xóa toàn bộ lịch sử"):
            save_logs([])
            st.toast("Đã xóa lịch sử")
            st.experimental_rerun()

        selected = st.selectbox("Chọn bản ghi để xem chi tiết:", df_logs.index)
        if selected is not None:
            log_detail = df_logs.loc[selected]
            st.markdown(f"**Người gửi:** {log_detail['sender']}")
            st.markdown(f"**Tiêu đề:** {log_detail['subject']}")
            st.markdown(f"**Kết luận:** {log_detail['verdict']}")
            st.markdown("**URLs nghi ngờ:**")
            if log_detail["urls"]:
                for u in log_detail["urls"]:
                    st.markdown(f"- {u}")
            else:
                st.markdown("_Không phát hiện link đáng ngờ_")
