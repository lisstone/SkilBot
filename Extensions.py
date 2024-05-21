import json
import requests
keys = {
    'евро' : "EUR",
    'доллар' : "USD",
    'рубль' : "RUR",
    'тенге' : "KZT",
}
class ValuePrice:
    @staticmethod
    def get_price(quote, base, amount):
        params = {
            'currency_from': keys[quote],
            'currency_to': keys[base],
            'source': 'cbrf',
            'sum': amount,
            'date': '',
        }

        response = requests.get('https://cash.rbc.ru/cash/json/converter_currency_rate/', params=params)
        data = json.loads(response.content)
        answer = data['data']['sum_result']
        return f"{amount} {keys[quote]} = {round(answer, 2)} {keys[base]}"

class ErrorTryEx(Exception):
    pass