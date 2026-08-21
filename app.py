import streamlit as st
import datetime

# Page configuration
st.set_page_config(page_title="O-Day Attendance / 出席登記", page_icon="📝", layout="centered")

# Bilingual Titles
st.title("🎓 Orientation Day Attendance Record")
st.subheader("出席登記")
st.write("Please enter your full name below to record your attendance.")
st.write("請在下方輸入您的全名以作出席記錄。")
st.markdown("---")

# Establish a connection to Google Sheets natively
try:
    conn = st.connection("gsheets", type="spreadsheet")
except Exception:
    conn = None

# Attendance Form
with st.form("attendance_form", clear_on_submit=True):
    
    student_name = st.text_input(
        "Full Name (English or Chinese) / 姓名 *", 
        placeholder="e.g. CHAN Tai Man / 陳大文"
    )
    
    submit_button = st.form_submit_button("Submit Attendance / 提交登記")

if submit_button:
    cleaned_name = student_name.strip()
    
    if not cleaned_name:
        st.error("❌ Please enter your name. / 請輸入您的姓名。")
    elif conn is None:
        st.error("❌ Connection configuration error. Please check your Secrets setup.")
        st.error("連線設定錯誤，請檢查 Secrets 設定。")
    else:
        try:
            # Fetch existing data using native connection
            existing_data = conn.read(ttl=0)
            
            # Create timestamp
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Structure new row
            new_row = {"Timestamp": current_time, "Name": cleaned_name}
            
            # Append natively and sync back to Google Sheets
            import pandas as pd
            new_entry_df = pd.DataFrame([new_row])
            
            if existing_data is None or existing_data.empty or existing_data.dropna(how='all').empty:
                updated_data = new_entry_df
            else:
                updated_data = pd.concat([existing_data, new_entry_df], ignore_index=True)
            
            # Update the sheet
            conn.update(data=updated_data)
            
            st.success(f"✅ Thank you, {cleaned_name}! Your attendance has been successfully recorded.")
            st.success(f"登記成功！謝謝您，{cleaned_name}。")
            
        except Exception as e:
            st.error("❌ Registration failed. Please contact the administrator.")
            st.error("登記失敗，請聯絡管理員。")
            st.exception(e)
