
import streamlit as st
import os
import datetime
import pandas as pd

st.set_page_config(page_title="青花瓷直笛自主練習平台", layout="centered")

UPLOAD_DIR = "uploads"
LOG_FILE = "upload_log.csv"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

view_mode = st.experimental_get_query_params().get("view", ["student"])[0]

if view_mode == "teacher":
    st.title("👩‍🏫 教師端：學生上傳紀錄")
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        st.dataframe(df)
        with open(LOG_FILE, "rb") as f:
            st.download_button("📥 下載 CSV 紀錄", f, file_name="upload_log.csv")
    else:
        st.warning("尚無任何學生上傳紀錄。")
else:
    st.title("🎵 青花瓷直笛自主練習平台")
    st.markdown("請依照以下步驟練習並上傳錄音：")

    st.video("https://youtu.be/BpK29uDMrD4")

    class_input = st.text_input("請輸入班級（如 501）")
    name_input = st.text_input("請輸入姓名")
    uploaded_file = st.file_uploader("請上傳您的錄音檔（mp3 或 m4a）", type=["mp3", "m4a"])

    if st.button("📤 上傳錄音"):
        if not all([class_input, name_input, uploaded_file]):
            st.warning("請完整填寫資料並上傳錄音檔。")
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = uploaded_file.name.split('.')[-1]
            filename = f"{class_input}_{name_input}_青花瓷_{timestamp}.{ext}"
            save_path = os.path.join(UPLOAD_DIR, filename)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"{class_input},{name_input},{timestamp},{filename},{save_path}\n")

            st.success("✅ 上傳成功！")
            st.audio(uploaded_file)
