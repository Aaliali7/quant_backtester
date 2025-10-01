import pandas as pd

def momentum_12_1(prices: pd.DataFrame, skip_days: int = 21, lookback_days: int = 252) -> pd.DataFrame:
    """
    Cross-sectional momentum (12-1): price(t-skip) / price(t-skip-lookback) - 1
    Typically skip ~1 month (~21 trading days) to avoid short-term reversal.
    """
    forward = prices.shift(skip_days)
    past = prices.shift(skip_days + lookback_days)
    mom = (forward / past) - 1.0
    return mom

def mean_reversion_5d(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Simple cross-sectional mean reversion proxy: negative 5-day return.
    Higher is 'more mean-reverting long' (i.e., recently sold off).
    """
    ret5 = prices.pct_change(5)
    return -ret5

def winsorize_cross_section(signal_row: pd.Series, lower_q: float = 0.01, upper_q: float = 0.99) -> pd.Series:
    lo = signal_row.quantile(lower_q)
    hi = signal_row.quantile(upper_q)
    return signal_row.clip(lower=lo, upper=hi)
