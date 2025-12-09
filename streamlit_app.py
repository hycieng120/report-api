import streamlit as st
import requests

st.title("📊 報表生成系統")

# 使用者輸入
symbol = st.text_input("股票代號 (symbol)", "AAPL")
returns = st.text_area("股票報酬率 (returns, 以逗號分隔)", "0.01,0.02,0.03")
benchmark = st.text_area("基準報酬率 (benchmark, 以逗號分隔)", "")

# 按鈕觸發
if st.button("生成報表"):
    # 將輸入轉換成數字陣列
    returns_list = [float(x.strip()) for x in returns.split(",") if x.strip()]
    benchmark_list = [float(x.strip()) for x in benchmark.split(",") if x.strip()]

    payload = {
        "symbol": symbol,
        "returns": returns_list,
        "stock_returns": returns_list,
        "benchmark": benchmark_list if benchmark_list else None
    }

    try:
        # 呼叫 Render 雲端 API
        api_url = "https://report-api.onrender.com/api/report"  # 改成你的 Render URL
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            data = response.json()
            st.success(data["message"])
            st.json(data["files"])
        else:
            st.error(f"API 錯誤: {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error(f"呼叫 API 發生錯誤: {e}")