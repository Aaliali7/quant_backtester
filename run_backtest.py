import pandas as pd
from src.data import load_universe, get_price_data
from src.factors import momentum_12_1, winsorize_cross_section
from src.backtest import long_short_backtest
from src.metrics import cagr, annual_vol, sharpe, max_drawdown, calmar, hit_rate
from src.plots import plot_equity_and_drawdown

from pathlib import Path

START = "2015-01-01"
END   = None  # uses today
COSTS_BPS = 5.0
TOP_Q = 0.2
BOTTOM_Q = 0.2

def main():
    universe = load_universe("data/universe.csv")
    print(f"Universe size: {len(universe)} tickers")

    prices = get_price_data(universe, start=START, end=END, interval="1d")
    prices = prices.dropna(how="all").ffill().dropna(axis=1, how="any")  # keep only clean histories

    # Build 12-1 momentum
    signal = momentum_12_1(prices)

    # Clean signal cross-sectionally each day (winsorize mild outliers)
    signal = signal.apply(winsorize_cross_section, axis=1)

    # Backtest
    res = long_short_backtest(
        prices=prices,
        signal=signal,
        top_q=TOP_Q,
        bottom_q=BOTTOM_Q,
        rebalance_freq="M",
        costs_bps=COSTS_BPS,
    )

    net = res["portfolio_returns"]["net"]
    eq  = res["equity"]["equity"]

    # Metrics
    summary = {
        "CAGR": cagr(net),
        "Ann Vol": annual_vol(net),
        "Sharpe (rf=0)": sharpe(net, rf=0.0),
        "Max Drawdown": max_drawdown(eq),
        "Calmar": calmar(net, eq),
        "Hit Rate": hit_rate(net),
        "Start": net.index.min().date() if len(net)>0 else None,
        "End": net.index.max().date() if len(net)>0 else None,
        "N Days": len(net),
    }
    print("\nPerformance Summary:")
    for k,v in summary.items():
        print(f"  {k:15s}: {v}")

    # Plots
    Path("figs").mkdir(exist_ok=True)
    plot_equity_and_drawdown(eq, "figs/momentum_ls.png")
    print("\nSaved plots to figs/")

if __name__ == "__main__":
    main()
