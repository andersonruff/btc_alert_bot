import os
import yfinance as yf
from ta.momentum import RSIIndicator
import requests
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RSI_ALERT = 30

if not TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN ou CHAT_ID não encontrados nos secrets")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def get_btc_data():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")
    data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()
    return data

def main():
    data = get_btc_data()
    latest = data.iloc[-1]
    price = latest['Close']
    rsi = latest['RSI']

    message = (
        f"📊 BTC Monitor\n"
        f"Preço: ${price:,.0f}\n"
        f"RSI(14): {rsi:.2f}\n"
        f"⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )

    if rsi < RSI_ALERT:
        message = "🚨 ALERTA DE SOBREVENDA\n\n" + message

    send_telegram(message)

if __name__ == "__main__":
    main()
