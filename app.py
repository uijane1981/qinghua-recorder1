import streamlit as st
import os
import datetime
import pandas as pd

# 設定標題與說明
st.set_page_config(page_title="青花瓷直笛自主練習平台", layout="centered")
st.title("🎵 青花瓷直笛自主練習平台")
st.write("請依照以下步驟練習並上傳錄音：")

# 嵌入 YouTube 教學影片
st.video("https://www.youtube.com/watch?v=BpK29uDMrD4")

# 使用者輸入欄位
class_name = st.text_input("請輸入班級（如 501）")
student_name = st.text_input("請輸入姓名")
uploaded_file = st.file_uploader("請上傳您的錄音檔（mp3 或 m4a）", type=["mp3", "m4a"])

# 儲存錄音檔與紀錄
if st.button("📩 上傳錄音"):
    if not class_name or not student_name or not uploaded_file:
        st.warning("請完整填寫資料並上傳錄音檔。")
    else:
        # 建立儲存資料夾
        os.makedirs("uploads", exist_ok=True)

        # 組合檔名：班級_姓名_時間
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = uploaded_file.name.split('.')[-1]
        filename = f"{class_name}_{student_name}_{now}.{ext}"
        filepath = os.path.join("uploads", filename)

        # 儲存錄音檔
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 紀錄上傳資料
        log_path = "upload_log.csv"
        if os.path.exists(log_path):
            df = pd.read_csv(log_path)
        else:
            df = pd.DataFrame(columns=["班級", "姓名", "檔名", "時間"])

        df.loc[len(df)] = [class_name, student_name, filename, now]
        df.to_csv(log_path, index=False, encoding="utf-8-sig")

        st.success("✅ 上傳成功！謝謝您的練習～")

# 教師檢視模式
params = st.query_params
if "view" in params and params["view"] == "teacher":
    st.header("👩‍🏫 教師端上傳紀錄")
    if os.path.exists("upload_log.csv"):
        df = pd.read_csv("upload_log.csv")
        st.dataframe(df)
    else:
        st.info("目前尚無學生上傳資料。")
