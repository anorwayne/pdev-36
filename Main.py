import telebot
import requests
import json
import config
from extensions import APIException

bot = telebot.TeleBot(config.TOKEN)

currencies = {
    "USD": "Доллар",
    "EUR": "Евро"
}


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, instructions)


instructions = "Добро пожаловать в бота для конвертации валют!\n\n" \
               "Используйте команду /values для получения списка доступных валют.\n" \
               "Для конвертации валюты используйте следующий формат сообщения:\n" \
               "<название первой валюты> <название второй валюты> <количество первой валюты>\n" \
               "Например: USD EUR 100\n\n" \
               "При возникновении ошибки, бот выдаст пояснение."


@bot.message_handler(commands=['values'])
def handle_values(message):
    currencies = "Доступные валюты:\n" \
                 "1. Доллар (USD)\n" \
                 "2. Евро (EUR)\n"

    bot.reply_to(message, currencies)


def get_price(base: str, quote: str, amount: float) -> float:
    global valute_data
    base = base.upper()
    quote = quote.upper()
    if base == quote:
        raise APIException("Вы ввели одинаковые валюты")

    if base not in currencies or quote not in currencies:
        raise APIException("Неправильно введена валюта")

    response = requests.get(f"https://www.cbr-xml-daily.ru/daily_json.js")
    data = json.loads(response.text)
    try:
        valute_data = data["Valute"]
        if base in valute_data and quote in valute_data:
            base_rate = valute_data[base]["Value"]
            quote_rate = valute_data[quote]["Value"]
            converted_amount = (amount * quote_rate) / base_rate
            return converted_amount
    except KeyError:
        raise APIException("Не удалось получить курс для указанных валют")


@bot.message_handler(commands=['values'])
def handle_values(message):
    available_currencies = "Доступные валюты:\n" \
                           "1. Доллар (USD)\n" \
                           "2. Евро (EUR)\n" \
                           "3. Рубль (RUB)"
    bot.reply_to(message, available_currencies)


@bot.message_handler(func=lambda message: len(message.text.split()) == 4)
def handle_conversion(message):
    try:
        base, quote, amount = message.text.split()
        amount = float(amount)
        converted_amount = get_price(base, quote, amount)
        result = f"{base} {quote} = {converted_amount} {amount}"
        bot.reply_to(message, result)
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e.message}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


bot.polling(none_stop=True)
