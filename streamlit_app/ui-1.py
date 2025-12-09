# streamlit_app/ui.py
import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Quant Backtest", layout="centered")
st.title("Quant Backtest Runner")

ticker = st.text_input("Ticker", "0050.TW")
benchmark = st.text_input("Benchmark", "2330.TW")

col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start", value=datetime.date(2024, 11, 1), format="YYYY-MM-DD")
with col2:
    end = st.date_input("End", value=datetime.date(2025, 12, 1), format="YYYY-MM-DD")

if st.button("Run backtest"):
    payload = {
        "ticker": ticker,
        "benchmark": benchmark,
        "start": start.strftime("%Y-%m-%d"),  # 確保是正確字串格式
        "end": end.strftime("%Y-%m-%d")
    }
    try:
        # 注意路由要加上 /api
        resp = requests.post("http://127.0.0.1:5000/api/analyze", json=payload, timeout=120)
        
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Status: {data['status']} | Log ID: {data['log_id']}")
            
            # 確認檔案存在再顯示下載按鈕
            for f in data.get("files", []):
                try:
                    with open(f, "rb") as file:
                        st.download_button(f"Download {f}", file, f)
                except FileNotFoundError:
                    st.warning(f"{f} not found.")
            
            if data.get("sent"):
                st.info("Email sent.")
            else:
                st.warning("Email not sent.")
        else:
            st.error(f"API error: {resp.status_code} {resp.text}")
    except Exception as e:
        st.error(f"Error: {e}")