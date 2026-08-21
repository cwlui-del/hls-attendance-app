import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 網頁基礎頁面設定
st.set_page_config(page_title="O-Day Attendance / 出席登記", page_icon="📝", layout="centered")

# 中英文雙語標題
st.title("🎓 Orientation Day Attendance Record")
st.subheader("出席登記")
st.write("Please enter your full name below to record your attendance.")
st.write("請在下方輸入您的全名以作出席記錄。")
st.markdown("---")

# 初始化 Google Sheets 雲端連接
conn = st.connection("gsheets", type=GSheetsConnection)

# 建立學生輸入表單
with st.form("attendance_form", clear_on_submit=True):
    
    # 僅記錄出席學生姓名欄位
    student_name = st.text_input(
        "Full Name (English or Chinese) / 姓名 *", 
        placeholder="e.g. CHAN Tai Man / 陳大文"
    )
    
    # 中英文提交按鈕
    submit_button = st.form_submit_button("Submit Attendance / 提交登記")

# 當學生點擊提交按鈕後的處理邏輯
if submit_button:
    # 清除文字前後多餘的空格
    cleaned_name = student_name.strip()
    
    if not cleaned_name:
        st.error("❌ Please enter your name. / 請輸入您的姓名。")
    else:
        try:
            # 1. 即時讀取現有的 Google Sheet 數據 (ttl=0 確保不讀取暫存舊資料)
            existing_data = conn.read(ttl=0)
            
            # 2. 自動獲取當前的系統精確日期與時間 (Timestamp)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 3. 將新數據包裝成 Pandas DataFrame
            new_entry = pd.DataFrame([{
                "Timestamp": current_time,
                "Name": cleaned_name
            }])
            
            # 4. 檢查舊數據是否為空，並將新紀錄合併到最下方
            if existing_data.empty or existing_data.dropna(how='all').empty:
                updated_data = new_entry
            else:
                updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
            
            # 5. 將整份更新後的數據重新推送到雲端 Google Sheet
            conn.update(data=updated_data)
            
            # 6. 畫面向學生展示中英文成功提示
            st.success(f"✅ Thank you, {cleaned_name}! Your attendance has been successfully recorded.")
            st.success(f"登記成功！謝謝您，{cleaned_name}。")
            
        except Exception as e:
            st.error("❌ Registration failed. Please contact the administrator.")
            st.error("登記失敗，請聯絡管理員。")
            st.exception(e)
