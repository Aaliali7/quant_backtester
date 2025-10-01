import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_and_drawdown(equity: pd.Series, out_path: str):
    eq = equity.dropna()
    if eq.empty:
        return
    # Equity
    plt.figure(figsize=(10,5))
    eq.plot()
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Net Asset Value")
    plt.tight_layout()
    plt.savefig(out_path.replace(".png", "_equity.png"))
    plt.close()

    # Drawdown
    peak = eq.cummax()
    dd = eq/peak - 1.0
    plt.figure(figsize=(10,5))
    dd.plot()
    plt.title("Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.tight_layout()
    plt.savefig(out_path.replace(".png", "_drawdown.png"))
    plt.close()
