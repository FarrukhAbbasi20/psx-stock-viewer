import datetime
import matplotlib.pyplot as plt
from src.psx import stocks

# List of bank tickers
bank_tickers = ["SILK", "JSBL", "BAFL", "MCB"]

# Fetch stock data for all banks
data = stocks(bank_tickers, start=datetime.date(2020, 1, 1), end=datetime.date.today())

# Show first few rows
print(data.head())

# Plot closing prices
plt.figure(figsize=(12, 6))
for ticker in bank_tickers:
    try:
        # Access hierarchical DataFrame
        plt.plot(data.loc[ticker].index, data.loc[ticker]["Close"], label=ticker)
    except KeyError:
        print(f"Data for {ticker} not available or 'Close' column missing.")

plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Bank Closing Prices Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
