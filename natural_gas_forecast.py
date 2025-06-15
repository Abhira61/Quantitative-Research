import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import datetime

# Load the data
df = pd.read_csv('natural_gas_prices.csv',parse_dates=['Date'])
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# Plot historical prices
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Price'], label='Historical Prices')
plt.title('Natural Gas Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.legend()
plt.show()

# Train the model and forecast 12 more months
model = ExponentialSmoothing(df['Price'], trend='add', seasonal='add', seasonal_periods=12)
fit = model.fit()
forecast = fit.forecast(12)

# Combine historical + forecast
full_data = pd.concat([df['Price'], forecast])

# Plot full picture
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Price'], label='Historical')
plt.plot(forecast.index, forecast, label='Forecast', linestyle='--')
plt.title('Natural Gas Prices (Historical + 1 Year Forecast)')
plt.xlabel('Dates')
plt.ylabel('Price')
plt.grid(True)
plt.legend()
plt.show()

# Estimation function
def estimate_gas_price(date_str):
    """Estimate gas price for a given date string (e.g., '2025-06-01')"""
    try:
        target_date = pd.to_datetime(date_str)
        if target_date in full_data.index:
            return float(full_data.loc[target_date])
        else:
            # Interpolate for dates between known months
            return float(full_data.reindex(full_data.index.union([target_date])).interpolate().loc[target_date])
    except Exception as e:
        return f"Error: {e}"

# Example usage
print("Estimated price on 2023-12-01:", estimate_gas_price("2023-12-01"))
print("Estimated price on 2025-06-01:", estimate_gas_price("2025-06-01"))
