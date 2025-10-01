# Quant Factor Backtester (Momentum)
Tests](https://github.com/Aaliali7/quant_backtester/actions/workflows/tests.yml/badge.svg)
End-to-end equity factor research pipeline in Python:
- Downloads prices (yfinance)
- Builds 12–1 momentum signal (skip 1 month)
- Long/short (top/bottom decile), monthly rebalance
- Turnover-based transaction costs
- Metrics: CAGR, vol, Sharpe, max DD, Calmar, hit rate
- Plots: equity & drawdown
- Pytest unit tests

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run_backtest.py

cat > README.md << 'EOF'
# Quant Factor Backtester (Momentum)

End-to-end equity factor research pipeline in Python:
- Downloads prices (yfinance)
- Builds 12–1 momentum signal (skip 1 month)
- Long/short (top/bottom decile), monthly rebalance
- Turnover-based transaction costs
- Metrics: CAGR, vol, Sharpe, max DD, Calmar, hit rate
- Plots: equity & drawdown
- Pytest unit tests

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run_backtest.py

cat > pytest.ini << 'EOF'
[pytest]
pythonpath = .
