import os
import yfinance as yf
import requests
from datetime import datetime
from ta.momentum import RSIIndicator

# ----- CONFIGURAÇÃO (VEM DO GITHUB SECRETS) -----
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_")  # se o seu secret realmente se chama CHAT_
RSI_ALERT = 30

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def get_btc_data():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")
    data["RSI"] = RSIIndicator(data["Close"], window=14).rsi()
    return data

def main():
    data = get_btc_data()
    latest = data.iloc[-1]
    price = latest["Close"]
    rsi = latest["RSI"]

    message = (
        f"🚀 BTC Monitor\n"
        f"Preço: ${price:,.0f}\n"
        f"RSI(14): {rsi:.2f}\n"
        f"⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )

    if rsi < RSI_ALERT:
        message = "🚨 ALERTA DE SOBREVENDA\n\n" + message

    send_telegram(message)

if __name__ == "__main__":
    main()
