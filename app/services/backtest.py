# app/services/backtest.py
import pandas as pd
import numpy as np   # 新增這行

def run_backtest(ticker: str, start: str, end: str):
    # Dummy backtest
    returns = pd.Series(np.random.randn(250)).cumsum()   # 改成 np
    positions = pd.DataFrame({"ticker": [ticker], "weight": [1.0]})
    transactions = []
    gross_lev = 1.0
    return returns, positions, transactions, gross_lev

'''# app/services/backtest.py
import pandas as pd

def run_backtest(ticker: str, start: str, end: str):
    # Dummy backtest
    returns = pd.Series(pd.np.random.randn(250)).cumsum()
    positions = pd.DataFrame({"ticker": [ticker], "weight": [1.0]})
    transactions = []
    gross_lev = 1.0
    return returns, positions, transactions, gross_lev
'''