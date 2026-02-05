import os
import yfinance as yf
from ta.momentum import RSIIndicator
import requests
from datetime import datetime
import time

# ----- CONFIGURAÇÃO -----
TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
RSI_ALERT = 30
CHECK_INTERVAL = 3600  # intervalo em segundos

# ----- FUNÇÃO DE ALERTA -----
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

# ----- BUSCAR PREÇOS BTC -----
def get_btc_data():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")
    data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()
    return data

# ----- AGENTE CONTÍNUO -----
alert_sent = False

while True:
    data = get_btc_data()
    latest = data.iloc[-1]
    price = latest['Close']
    rsi = latest['RSI']

    if rsi < RSI_ALERT and not alert_sent:
        message = f"🚨 ALERTA BTC\nPreço: ${price:,.0f}\nRSI(14): {rsi:.2f}\nCondição: Sobrevenda\n⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        send_telegram(message)
        alert_sent = True
    elif rsi >= RSI_ALERT:
        alert_sent = False

    print(f"Preço atual: ${price:,.0f}, RSI: {rsi:.2f}")
    time.sleep(CHECK_INTERVAL)
