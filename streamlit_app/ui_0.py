# streamlit_app/ui.py
import streamlit as st
import requests

st.set_page_config(page_title="Quant Backtest", layout="centered")
st.title("Quant Backtest Runner")

ticker = st.text_input("Ticker", "0050.TW")
benchmark = st.text_input("Benchmark", "2330.TW")
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start", value=None, format="YYYY-MM-DD")
with col2:
    end = st.date_input("End", value=None, format="YYYY-MM-DD")

if st.button("Run backtest"):
    payload = {
        "ticker": ticker,
        "benchmark": benchmark,
        "start": str(start),
        "end": str(end)
    }
    try:
        resp = requests.post("http://127.0.0.1:5000/analyze", json=payload, timeout=120)
        data = resp.json()
        st.success(f"Status: {data['status']} | Log ID: {data['log_id']}")
        st.download_button("Download report.pdf", open("report.pdf", "rb"), "report.pdf")
        st.download_button("Download compare.pdf", open("compare.pdf", "rb"), "compare.pdf")
        if data.get("sent"):
            st.info("Email sent.")
        else:
            st.warning("Email not sent.")
    except Exception as e:
        st.error(f"Error: {e}")