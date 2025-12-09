# app/api/routes.py
from flask import Blueprint, request, jsonify, send_file
from app.services.data_loader import get_stock_returns
from app.services.backtest import run_backtest
from app.services.report import generate_report, compare_with_benchmark
from app.services.emailer import send_report
from app.services.logger import log_analysis
from app.config import Settings
import os

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

api = Blueprint("api", __name__)
'''
@api.route("/report", methods=["POST"])
def report():
    data = request.get_json()
    symbol = data.get("symbol")
    start = data.get("start")
    end = data.get("end")

    try:
        # 生成主要報表
        # report_file = generate_report(symbol, start, end)
        report_file = generate_report(
            symbol,
            data.get("returns", [])
)


        # 如果有 benchmark 資料，就生成比較報表
        compare_file = ""
        benchmark = data.get("benchmark")
        stock_returns = data.get("stock_returns", [])
        if benchmark:
            compare_file = compare_with_benchmark(stock_returns, benchmark)

        return jsonify({
            "message": "Reports generated successfully",
            "files": {
                "report": report_file,
                "compare": compare_file
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''
@api.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "GET":
        # 瀏覽器直接打開時，回傳提示訊息
        return jsonify({"message": "Use POST with JSON body to generate reports"})

    if request.method == "POST":
        data = request.get_json()
        symbol = data.get("symbol")
        returns = data.get("returns", [])
        start = data.get("start")
        end = data.get("end")

        try:
            # 生成主要報表
            report_file = generate_report(symbol, returns, "reort.pdf")

            # 如果有 benchmark 資料，就生成比較報表
            compare_file = ""
            benchmark = data.get("benchmark")
            stock_returns = data.get("stock_returns", [])
            if benchmark:
                compare_file = compare_with_benchmark(stock_returns, benchmark, "compare.pdf")

            return jsonify({
                "message": "Reports generated successfully",
                "files": {
                    "report": report_file,
                    "compare": compare_file
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
'''@api.route("/report", methods=["POST"])
def report():
    data = request.get_json()
    symbol = data.get("symbol")
    start = data.get("start")
    end = data.get("end")

    # 呼叫報表生成邏輯
    pdf_path = generate_report(symbol, start, end)

    return jsonify({"message": "Report generated", "file": pdf_path})
'''
@api.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True) or {}
    ticker = data.get("ticker", "0050.TW")
    benchmark = data.get("benchmark", "2330.TW")
    start = data.get("start", "2015-01-01")
    end = data.get("end", "2023-12-31")

    stock_returns = get_stock_returns(ticker, start, end)
    benchmark_returns = get_stock_returns(benchmark, start, end)

    compare_with_benchmark(stock_returns, benchmark_returns, filename="compare.pdf")
    returns, positions, transactions, gross_lev = run_backtest(ticker, start, end)
    generate_report(ticker, returns, positions, transactions, "report.pdf")

    #generate_report(returns, positions, transactions, filename="report.pdf")

    log_id = log_analysis(ticker, benchmark, start, end, ["report.pdf", "compare.pdf"])

    try:
        send_report(
            Settings.MAIL_FROM, Settings.MAIL_TO,
            Settings.SMTP_HOST, Settings.SMTP_PORT,
            Settings.SMTP_USER, Settings.SMTP_PASS,
            ["report.pdf", "compare.pdf"]
        )
        sent = True
    except Exception as e:
        sent = False

    return jsonify({
        "status": "success",
        "log_id": log_id,
        "sent": sent,
        "files": ["report.pdf", "compare.pdf"]
    })
    
@api.route("/download/<filename>", methods=["GET"])
def download(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": f"{filename} not found"}), 404

