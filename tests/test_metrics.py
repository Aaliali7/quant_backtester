import pandas as pd
import numpy as np
from src.metrics import cagr, annual_vol, sharpe, max_drawdown, calmar, hit_rate

def test_cagr_known():
    # If returns are constant r each day, equity grows (1+r)^N
    r = 0.001
    N = 252*2
    s = pd.Series([r]*N)
    out = cagr(s)
    # CAGR should be close to (1+r)^(252) - 1 for one year equivalent
    approx_yr = (1+r)**252 - 1
    assert abs(out - approx_yr) < 1e-3

def test_max_drawdown_basic():
    eq = pd.Series([1, 1.2, 1.1, 1.3, 1.0, 1.5])
    mdd = max_drawdown(eq)
    # Peak at 1.3 to trough at 1.0 -> drawdown = 1.0/1.3 - 1 = -0.2307...
    assert abs(mdd - (1.0/1.3 - 1)) < 1e-6

def test_hit_rate():
    s = pd.Series([1, -1, 0, 2, -3])
    hr = hit_rate(s)
    assert abs(hr - (2/5)) < 1e-6
