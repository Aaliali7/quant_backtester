import numpy as np
import pandas as pd

def cagr(returns: pd.Series, periods_per_year: int = 252) -> float:
    r = returns.dropna()
    if r.empty:
        return np.nan
    cum = (1 + r).prod()
    yrs = len(r) / periods_per_year
    if yrs == 0:
        return np.nan
    return cum ** (1 / yrs) - 1

def annual_vol(returns: pd.Series, periods_per_year: int = 252) -> float:
    r = returns.dropna()
    return r.std() * np.sqrt(periods_per_year) if len(r)>1 else np.nan

def sharpe(returns: pd.Series, rf: float = 0.0, periods_per_year: int = 252) -> float:
    r = returns.dropna()
    if r.empty:
        return np.nan
    excess = r - (rf / periods_per_year)
    mu = excess.mean() * periods_per_year
    sig = excess.std() * np.sqrt(periods_per_year)
    return mu / sig if sig and not np.isnan(sig) and sig!=0 else np.nan

def max_drawdown(equity: pd.Series) -> float:
    x = equity.dropna().values
    if len(x) == 0:
        return np.nan
    peaks = np.maximum.accumulate(x)
    dd = (x / peaks) - 1.0
    return dd.min()

def calmar(returns: pd.Series, equity: pd.Series, periods_per_year: int = 252) -> float:
    c = cagr(returns, periods_per_year)
    mdd = abs(max_drawdown(equity))
    return c / mdd if mdd and not np.isnan(mdd) and mdd!=0 else np.nan

def hit_rate(returns: pd.Series) -> float:
    r = returns.dropna()
    if r.empty:
        return np.nan
    return (r > 0).mean()
