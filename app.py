from flask import Flask, request, jsonify
import psycopg2
import os

# 建立 Flask API
api = Flask(__name__)

# 連接 Postgres (Render 會自動注入 DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# 模擬報表生成函式
def generate_report(symbol, returns):
    # 這裡可以用 pandas/matplotlib/weasyprint 生成 PDF
    # 暫時回傳檔名
    return "report.pdf"

def compare_with_benchmark(stock_returns, benchmark):
    # 這裡可以做 benchmark 比較並生成 PDF
    return "compare.pdf"

@api.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "GET":
        return jsonify({"message": "Use POST with JSON body to generate reports"})

    if request.method == "POST":
        data = request.get_json()
        symbol = data.get("symbol")
        returns = data.get("returns", [])
        stock_returns = data.get("stock_returns", [])
        benchmark = data.get("benchmark")

        try:
            # 生成主要報表
            report_file = generate_report(symbol, returns)

            # 如果有 benchmark 資料，就生成比較報表
            compare_file = ""
            if benchmark:
                compare_file = compare_with_benchmark(stock_returns, benchmark)

            return jsonify({
                "message": "Reports generated successfully",
                "files": {
                    "report": report_file or "",
                    "compare": compare_file or ""
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Render 部署時用 gunicorn 啟動： gunicorn app:api
if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000)