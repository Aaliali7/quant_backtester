import pandas as pd
import yfinance as yf
from typing import List, Optional

def load_universe(csv_path: str) -> List[str]:
    df = pd.read_csv(csv_path)
    tickers = [t.strip().upper() for t in df["ticker"].dropna().unique().tolist()]
    return tickers

def get_price_data(tickers: List[str], start: str, end: Optional[str] = None, interval: str = "1d") -> pd.DataFrame:
    """
    Downloads Adjusted Close prices for the given tickers.
    Returns a DataFrame indexed by date with one column per ticker.
    """
    if end is None:
        end = pd.Timestamp.today().date().isoformat()
    df = yf.download(tickers, start=start, end=end, interval=interval, auto_adjust=False, progress=False)["Adj Close"]
    # If single ticker, make it DataFrame
    if isinstance(df, pd.Series):
        df = df.to_frame()
    # Ensure column names exactly match tickers (yfinance may return fewer)
    df = df.dropna(how="all", axis=1)
    df = df.sort_index()
    return df
