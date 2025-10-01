import numpy as np
import pandas as pd
from typing import Tuple, Dict

def _quantile_mask(row: pd.Series, top_q: float, bottom_q: float) -> Tuple[pd.Series, pd.Series]:
    ranks = row.rank(ascending=False, method="first")  # higher signal = better rank
    n = ranks.count()
    if n == 0:
        false_mask = pd.Series(False, index=row.index)
        return false_mask, false_mask
    top_k = int(np.ceil(n * top_q))
    bot_k = int(np.ceil(n * bottom_q))
    top_mask = ranks <= top_k
    bottom_mask = ranks > (n - bot_k)
    return top_mask, bottom_mask

def long_short_backtest(prices: pd.DataFrame,
                        signal: pd.DataFrame,
                        top_q: float = 0.1,
                        bottom_q: float = 0.1,
                        rebalance_freq: str = "ME",   # month-end
                        costs_bps: float = 10.0) -> Dict[str, pd.DataFrame]:

    prices = prices.sort_index()
    signal = signal.reindex_like(prices)
    returns = prices.pct_change().fillna(0.0)

    # Monthly snapshots of the signal (month-end can fall on weekends)
    sig_m = signal.resample(rebalance_freq).last().dropna(how="all")

    w_at_rebal = {}
    prev_w = pd.Series(0.0, index=prices.columns, dtype=float)

    for d in sig_m.index:
        # Snap to first trading day >= d
        i = prices.index.searchsorted(d, side="left")
        if i >= len(prices.index):
            break
        trade_day = prices.index[i]

        s = sig_m.loc[d].dropna()
        if s.empty:
            w_at_rebal[trade_day] = prev_w.copy()
            continue

        top_mask, bottom_mask = _quantile_mask(s, top_q, bottom_q)
        long_names = s[top_mask].index
        short_names = s[bottom_mask].index

        w = pd.Series(0.0, index=prices.columns, dtype=float)
        if len(long_names) > 0:
            w.loc[long_names] =  1.0 / max(1, len(long_names))
        if len(short_names) > 0:
            w.loc[short_names] = -1.0 / max(1, len(short_names))

        # Make portfolio ~market-neutral (0.5 long, 0.5 short)
        if (w > 0).any() and (w < 0).any():
            pos = w[w > 0].sum()
            neg = -w[w < 0].sum()
            if pos > 0:
                w[w > 0] *= 0.5 / pos
            if neg > 0:
                w[w < 0] *= 0.5 / neg

        w_at_rebal[trade_day] = w
        prev_w = w

    # Expand to daily weights by forward-fill
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    if w_at_rebal:
        wdf = pd.DataFrame.from_dict(w_at_rebal, orient="index").sort_index()
        weights.loc[wdf.index] = wdf.values
    weights = weights.replace(0.0, np.nan).ffill().fillna(0.0)

    gross_returns = (weights.shift(1) * returns).sum(axis=1)

    dw = weights.diff().abs().sum(axis=1).fillna(0.0)
    daily_cost = dw * (costs_bps / 1e4)

    net_returns = gross_returns - daily_cost
    equity = (1.0 + net_returns).cumprod()

    return {
        "weights": weights,
        "gross_returns": gross_returns.to_frame("gross"),
        "costs": daily_cost.to_frame("costs"),
        "portfolio_returns": net_returns.to_frame("net"),
        "equity": equity.to_frame("equity"),
    }
