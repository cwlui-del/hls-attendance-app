import streamlit as st
import datetime
import requests

# 網頁基礎頁面設定
st.set_page_config(page_title="O-Day Attendance / 出席登記", page_icon="📝", layout="centered")

# 中英文雙語標題
st.title("🎓 Orientation Day Attendance Record")
st.subheader("出席登記")
st.write("Please enter your full name below to record your attendance.")
st.write("請在下方輸入您的全名以作出席記錄。")
st.markdown("---")

# ==========================================================
# ⚠️ 請在此處填入你剛剛在第二步獲取的 Google 表單隱藏資料！
# ==========================================================
FORM_URL = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSdjGvXPf9S8-8L6OgK-EFKoKJfqToQfAKuaDWgua_nbPqX9ig/formResponse"
ENTRY_ID = "entry.126536379"
# ==========================================================

# 建立學生輸入表單
with st.form("attendance_form", clear_on_submit=True):
    
    student_name = st.text_input(
        "Full Name (English or Chinese) / 姓名 *", 
        placeholder="e.g. CHAN Tai Man / 陳大文"
    )
    
    submit_button = st.form_submit_button("Submit Attendance / 提交登記")

# 當學生點擊提交按鈕後的處理邏輯
if submit_button:
    cleaned_name = student_name.strip()
    
    if not cleaned_name:
        st.error("❌ Please enter your name. / 請輸入您的姓名。")
    elif "你的表單唯一ID" in FORM_URL:
        st.error("❌ System Configuration Error: Developer forgot to update Form URL.")
        st.error("系統設定錯誤：管理員尚未更換網頁代碼中的 FORM_URL。")
    else:
        try:
            # 準備發送給 Google 表單的數據封包
            # Google 表單會自動幫我們生成精確的提交時間（Timestamp），因此我們只需要傳送姓名
            payload = {ENTRY_ID: cleaned_name}
            
            # 在後台悄悄發送 POST 請求給 Google 表單
            response = requests.post(FORM_URL, data=payload)
            
            # 只要 Google 回應狀態碼為 200，代表 100% 寫入成功！
            if response.status_code == 200:
                st.success(f"✅ Thank you, {cleaned_name}! Your attendance has been successfully recorded.")
                st.success(f"登記成功！謝謝您，{cleaned_name}。")
            else:
                st.error("❌ Connection timed out. Please try again.")
                st.error("連線超時，請重新提交。")
                
        except Exception as e:
            st.error("❌ Network error. Please contact the administrator.")
            st.error("網路錯誤，請聯絡管理員。")
