import telebot
from telebot import types
from extensions import CurrencyConverter, APIException


bot = telebot.TeleBot('7136542240:AAFCpME7YlEpxlRspAq0v9uvjvGYwk4ktN8')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для конвертации валют.\n"
                            "Введи команду в формате: `<валюта_из> <валюта_в> <количество>` \n"
                            "Например: `USD EUR 10`\n"
                            "Для списка доступных валют используй /values")

@bot.message_handler(commands=['values'])
def get_values(message):
    bot.reply_to(message, "Доступные валюты: USD, EUR, RUB (Пока что только эти)")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        base, quote, amount_str = message.text.split()
        amount = float(amount_str)
        result = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        bot.reply_to(message, f"{amount} {base.upper()} = {result} {quote.upper()}")
    except ValueError:
        bot.reply_to(message, "Неверный формат ввода. Используйте `<валюта_из> <валюта_в> <количество>`")
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")


bot.infinity_polling()

