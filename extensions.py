import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Вызывает HTTPError для плохих ответов (4xx или 5xx)
            data = response.json()
            if 'rates' not in data:
                raise APIException("Неверный формат ответа API: Отсутствует ключ 'rates'")
            if quote not in data['rates']:
                raise APIException(f"Несуществующая валюта: {quote}")
            rate = data['rates'][quote]
            return round(amount * rate, 2)
        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка сети: {e}")
        except json.JSONDecodeError as e:
            raise APIException(f"Ошибка JSON: {e}")
        except KeyError as e:
            raise APIException(f"Неверный формат ответа API: {e}")
        except Exception as e:
            raise APIException(f"Неизвестная ошибка: {e}")


