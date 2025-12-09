# app/services/data_loader.py
import pandas as pd
import numpy as np   # 新增這行

def get_stock_returns(symbol: str, start: str, end: str) -> pd.Series:
    # TODO: replace with real data source
    idx = pd.date_range(start, end, freq="B")
    return pd.Series(np.random.randn(len(idx)).cumsum(), index=idx).pct_change().dropna()

'''# app/services/data_loader.py
import pandas as pd

def get_stock_returns(symbol: str, start: str, end: str) -> pd.Series:
    # TODO: replace with real data source
    idx = pd.date_range(start, end, freq="B")
    return pd.Series(pd.Series(pd.np.random.randn(len(idx))).cumsum(), index=idx).pct_change().dropna()
'''