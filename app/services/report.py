# app/services/report.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import base64
import io
import matplotlib.pyplot as plt

TEMPLATES = Path(__file__).parent.parent / "templates"

def render_pdf(template: str, context: dict, out_path: str):
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    html = env.get_template(template).render(context)
    HTML(string=html).write_pdf(out_path)
    return out_path
'''
def generate_report(returns, positions, transactions, filename="report.pdf"):
    return render_pdf("report.html", {"returns": list(returns)}, filename)
'''
'''
def generate_report(returns, positions=None, transactions=None, filename="report.pdf"):
    chart = plot_returns(returns)
    return render_pdf("report.html", {
        "returns": list(returns),
        "chart": chart
    }, filename)
'''

def generate_report(symbol, returns, positions=None, transactions=None, filename="report.pdf"):
    chart = plot_returns(returns)
    return render_pdf("report.html", {
        "symbol": symbol,
        "returns": list(returns),
        "positions": positions.to_dict(orient="records") if positions is not None else [],
        "transactions": transactions if transactions is not None else [],
        "chart": chart
    }, filename)

'''
def generate_report(symbol, returns, filename="report.pdf"):
    chart = plot_returns(returns)
    return render_pdf("report.html", {
        "symbol": symbol,
        "returns": list(returns),
        "chart": chart
    }, filename)
'''

'''def compare_with_benchmark(stock_returns, benchmark_returns, filename="compare.pdf"):
    return render_pdf("compare.html", {
        "stock": list(stock_returns),
        "benchmark": list(benchmark_returns)
    }, filename)
'''
'''
def compare_with_benchmark(stock_returns, benchmark_returns, filename="compare.pdf"):
    pairs = list(zip(stock_returns, benchmark_returns))
    return render_pdf("compare.html", {
        "pairs": pairs
    }, filename)
'''

def compare_with_benchmark(stock_returns, benchmark_returns, filename="compare.pdf"):
    pairs = list(zip(stock_returns, benchmark_returns))
    chart = plot_comparison(stock_returns, benchmark_returns)
    return render_pdf("compare.html", {
        "pairs": pairs,
        "chart": chart
    }, filename)
       
def plot_returns(returns):
    fig, ax = plt.subplots()
    ax.plot(range(len(returns)), returns, marker="o", linestyle="-", color="blue")
    ax.set_title("Returns Over Time")
    ax.set_xlabel("Index")
    ax.set_ylabel("Return")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def plot_comparison(stock_returns, benchmark_returns):
    fig, ax = plt.subplots()
    ax.plot(range(len(stock_returns)), stock_returns, marker="o", linestyle="-", color="blue", label="Stock")
    ax.plot(range(len(benchmark_returns)), benchmark_returns, marker="x", linestyle="--", color="red", label="Benchmark")
    ax.set_title("Stock vs Benchmark Returns")
    ax.set_xlabel("Index")
    ax.set_ylabel("Return")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")