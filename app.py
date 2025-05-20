
import streamlit as st
import os
import datetime
import pandas as pd

st.set_page_config(page_title="青花瓷直笛練習平台", layout="centered")

UPLOAD_DIR = "uploads"
LOG_FILE = "upload_log.csv"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# 初始化紀錄檔
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("班級,姓名,時間,檔名\n")

params = st.query_params
view_mode = params.get("view", ["student"])[0]

if view_mode == "teacher":
    st.title("👩‍🏫 教師端：學生上傳紀錄與錄音播放")
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        st.dataframe(df)

        # 播放每筆錄音檔
        st.subheader("▶️ 學生錄音檔播放")
        for index, row in df.iterrows():
            filepath = os.path.join(UPLOAD_DIR, row["檔名"])
            if os.path.exists(filepath):
                st.markdown(f"**{row['班級']} - {row['姓名']}** 上傳於 {row['時間']}")
                st.audio(filepath)
            else:
                st.warning(f"⚠️ 找不到檔案：{row['檔名']}")

        with open(LOG_FILE, "rb") as f:
            st.download_button("📥 下載上傳紀錄 CSV", f, file_name="upload_log.csv")
    else:
        st.warning("尚無任何學生上傳紀錄。")

else:
    st.title("🎵 青花瓷直笛練習平台")
    st.markdown("請依下列步驟操作：")

    st.video("https://youtu.be/BpK29uDMrD4")

    class_id = st.text_input("請輸入班級（如 501）")
    student_name = st.text_input("請輸入姓名")
    uploaded_file = st.file_uploader("請上傳錄音檔（mp3 或 m4a）", type=["mp3", "m4a"])

    if uploaded_file and class_id and student_name:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = uploaded_file.name.split('.')[-1]
        filename = f"{class_id}_{student_name}_{now}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{class_id},{student_name},{now},{filename}\n")

        st.success("✅ 上傳成功！錄音檔已儲存。")
        st.audio(uploaded_file)
    else:
        st.info("請輸入班級與姓名，並選擇錄音檔進行上傳。")
