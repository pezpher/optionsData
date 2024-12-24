import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Input tickers
tickers = input('Enter tickers separated by commas: ').split(',')

# Fetch expiration dates
def get_expiration_dates(ticker):
    option_chain = yf.Ticker(ticker).options
    return option_chain

# Get common expiration date and quantity of strikes
expiration_dates = get_expiration_dates(tickers[0])
for i, date in enumerate(expiration_dates):
    print(f"{i}. {date}")

# Select the expiration date of interest
selected_date_index = int(input('What expiration date? '))
selected_date = expiration_dates[selected_date_index]

# Get common quantity of strikes
stks = int(input('How many strikes? '))

# Create an empty list to store all the data
all_data = []

for ticker in tickers:
    # Fetch option data
    option_chain = yf.Ticker(ticker).option_chain(selected_date)
    calls = option_chain.calls
    puts = option_chain.puts

    # Get current stock price
    stock_price = round(yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1],2)

    # Separate options into Out-Of-The-Money (OTM) for calls
    otm_calls = calls[calls['strike'] >= stock_price].head(stks)[['strike', 'lastPrice', 'openInterest']]

    # Separate options into Out-Of-The-Money (OTM) for puts
    otm_puts = puts[puts['strike'] <= stock_price].tail(stks)[['strike', 'lastPrice', 'openInterest']]

    # Add a new column for the ratio of Last Price to Strike as a percentage (rounded to one decimal point)
    otm_calls['Return %'] = round((otm_calls['lastPrice'] / otm_calls['strike']) * 100, 2)
    otm_puts['Return %'] = round((otm_puts['lastPrice'] / otm_puts['strike']) * 100, 2)

    # Add a new column for the percentage move needed for the stock to reach the strike price
    otm_calls['Move Needed %'] = round(((otm_calls['strike'] - stock_price) / stock_price) * 100, 1)
    otm_puts['Move Needed %'] = round(((stock_price - otm_puts['strike']) / stock_price) * 100, 1)

    # Add a new column for the ratio of Move Needed % to Return %
    otm_calls['Move Needed/Return'] = round(otm_calls['Move Needed %'] / otm_calls['Return %'], 2)
    otm_puts['Move Needed/Return'] = round(otm_puts['Move Needed %'] / otm_puts['Return %'], 2)
    
    # Add a new column for the change of in Return %
    otm_calls['Change R%'] = round(otm_calls['Return %'] - otm_calls['Return %'].shift(-1), 2)
    otm_puts['Change R%'] = round(otm_puts['Return %'] - otm_puts['Return %'].shift(1), 2)
    
    # Add a new column for the change of slope in price
    otm_calls['Change P'] = round(otm_calls['lastPrice'] - otm_calls['lastPrice'].shift(-1), 2)
    otm_puts['Change P'] = round(otm_puts['lastPrice'] - otm_puts['lastPrice'].shift(1), 2)
                                 
    # Print OTM options for both calls and puts along with the expiration date
    print(f'OTM Put Options {selected_date} for {ticker}:')
    print(otm_puts.to_string(index=False))
    print(f'CMV={stock_price}')
    print(f'OTM Call Options {selected_date} for {ticker}:')
    print(otm_calls.to_string(index=False))

    # Append the current data to the overall list
    all_data.append({'Ticker': ticker, 'OTM Calls': otm_calls, 'OTM Puts': otm_puts})

# Plot for OTM Puts
plt.figure(figsize=(10, 6))
for data in all_data:
    plt.plot(data['OTM Puts']['Return %'], data['OTM Puts']['Move Needed %'], marker='o', label=f'{data["Ticker"]} - OTM Puts')

plt.title(f'Comparison of OTM Puts for {", ".join(tickers)} - {selected_date}')
plt.xlabel('Return %')
plt.ylabel('Move Needed %')
plt.legend()
plt.grid(True)

# Plot for OTM Calls
plt.figure(figsize=(10, 6))
for data in all_data:
    plt.plot(data['OTM Calls']['Return %'], data['OTM Calls']['Move Needed %'], marker='o', label=f'{data["Ticker"]} - OTM Calls')

plt.title(f'Comparison of OTM Calls for {", ".join(tickers)} - {selected_date}')
plt.xlabel('Return %')
plt.ylabel('Move Needed %')
plt.legend()
plt.grid(True)


# plot for Change
plt.figure(figsize=(10, 6))
for data in all_data:
    plt.plot(data['OTM Puts']['strike'], data['OTM Puts']['Change R%'], marker='o', label=f'{data["Ticker"]} - OTM Puts')
plt.title(f'Comparison of Change for {", ".join(tickers)} - {selected_date}')
plt.xlabel('strike')
plt.ylabel('Slope R%')
plt.legend()
plt.grid(True)


plt.figure(figsize=(10, 6))
for data in all_data:
    plt.plot(data['OTM Calls']['strike'], data['OTM Calls']['Change R%'], marker='o', label=f'{data["Ticker"]} - OTM Calls')
plt.title(f'Comparison of Change for {", ".join(tickers)} - {selected_date}')
plt.xlabel('strike')
plt.ylabel('Slope R%')
plt.legend()
plt.grid(True)

plt.show()
