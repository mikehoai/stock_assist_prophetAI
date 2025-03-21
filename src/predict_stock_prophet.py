import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.dates as mdates

def get_crypto_data(ticker, period, interval):
    crypto = yf.Ticker(ticker)
    data = crypto.history(period=period, interval=interval)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.tz_localize(None)  # Loại bỏ thông tin về múi giờ
    data = data[['Date', 'Close']]
    data.columns = ['ds', 'y']
    return data

def predict_crypto_price(data, periods, freq):
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)
    return forecast

def plot_forecast(data, forecast):
    plt.figure(figsize=(10, 6))
    
    future_forecast = forecast[forecast['ds'] > data['ds'].max()]
    
    plt.plot(future_forecast['ds'], future_forecast['yhat'], label='Predicted Price')
    plt.fill_between(future_forecast['ds'], future_forecast['yhat_lower'], future_forecast['yhat_upper'], color='gray', alpha=0.2)
    
    plt.scatter(future_forecast['ds'], future_forecast['yhat'], color='red', s=10)
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{mdates.num2date(sel.target[0]):%d/%m/%y}\nPrice: {sel.target[1]:.2f}"))

    plt.show()

if __name__ == "__main__":
    ticker = 'TSLA'
    period = '5y'
    interval = '1d'
    periods = 30 
    freq = 'D'

    data = get_crypto_data(ticker, period, interval)
    forecast = predict_crypto_price(data, periods, freq)
    plot_forecast(data, forecast)
