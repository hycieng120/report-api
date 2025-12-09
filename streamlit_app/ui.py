import streamlit as st
import requests

st.title("Quant Backtest Runner")

ticker = st.text_input("Ticker", "0050.TW")
benchmark = st.text_input("Benchmark", "2330.TW")
start = st.date_input("Start")
end = st.date_input("End")

if st.button("Run backtest"):
    payload = {
        "ticker": ticker,
        "benchmark": benchmark,
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d")
    }
    resp = requests.post("http://127.0.0.1:5000/api/analyze", json=payload)
    data = resp.json()

    st.success(f"Status: {data['status']} | Log ID: {data['log_id']}")

    for f in data.get("files", []):
        file_url = f"http://127.0.0.1:5000/api/download/{f}"
        file_resp = requests.get(file_url)
        if file_resp.status_code == 200:
            st.download_button(f"Download {f}", file_resp.content, f)
        else:
            st.warning(f"{f} not found on server.")

    if data.get("sent"):
        st.info("Email sent.")
    else:
        st.warning("Email not sent.")