import os
import telebot
import requests

API_TOKEN = os.getenv("API_TOKEN")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

bot = telebot.TeleBot(API_TOKEN)

def get_crypto_price(name):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={name}&vs_currencies=usd"
        r = requests.get(url)
        data = r.json()
        if name in data:
            return data[name]["usd"]
        return None
    except:
        return None

def get_stock_price(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        r = requests.get(url)
        data = r.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return float(data["Global Quote"]["05. price"])
        return None
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "📊 Bot Finanza attivo!\nUsa:\n/price bitcoin\n/price AAPL")

@bot.message_handler(commands=['price'])
def price(message):
    try:
        asset = message.text.split()[1]

        crypto = get_crypto_price(asset.lower())
        if crypto:
            bot.reply_to(message, f"💰 {asset.upper()} = ${crypto}")
            return

        stock = get_stock_price(asset.upper())
        if stock:
            bot.reply_to(message, f"📈 {asset.upper()} = ${stock}")
            return

        bot.reply_to(message, "❌ Asset non trovato")

    except:
        bot.reply_to(message, "Uso corretto: /price bitcoin")

print("BOT AVVIATO")
bot.infinity_polling()
