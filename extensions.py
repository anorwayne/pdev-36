import requests
import json


class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        base = base.upper()
        quote = quote.upper()
        if base == quote:
            raise APIException("Вы ввели одинаковые валюты")

        if base not in currencies or quote not in currencies:
            raise APIException("Неправильно введена валюта")

        response = requests.get(f"https://www.cbr-xml-daily.ru/daily_json.js")
        data = response.json()
        if "Valute" in data:
            valute_data = data["Valute"]
            if base in valute_data and quote in valute_data:
                base_rate = valute_data[base]["Value"]
                quote_rate = valute_data[quote]["Value"]
                converted_amount = (amount * quote_rate) / base_rate
                return converted_amount
                raise APIException("Не удалось получить курс для указанных валют")

        exchange_rate = data["rates"].get(quote)

        if exchange_rate is None:
            raise APIException("Не удалось получить курс для указанной валюты")
            converted_amount = amount * exchange_rate
            return converted_amount
