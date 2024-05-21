import Key
import telebot
import Extensions as EX

bot = telebot.TeleBot(Key.telega)

keys = EX.keys

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nУвидеть список всех доступных валют:\n/values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Валюты:'
    for valut in list(keys):
        text += "".join(f"\n{valut}")
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def send(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) < 3:
            raise EX.ErrorTryEx("Слишком мало параметров!")
        if len(values) > 3:
            raise EX.ErrorTryEx("Слишком много параметров!")
        quote, base, amount = values
        quote = str(quote).lower()
        base = str(base).lower()
        try:
            a = float(amount)
        except ValueError:
            a = amount
        if type(a) is str:
            raise EX.ErrorTryEx(f"Ожидалось число а не - ({a})")
        if quote == base:
            raise EX.ErrorTryEx(f"Параметры должны быть разные")
        if quote not in list(keys):
            raise EX.ErrorTryEx(f"Нет такого параметра как - ({quote})")
        if base not in list(keys):
            raise EX.ErrorTryEx(f"Нет такого параметра как - ({base})")
        price = EX.ValuePrice.get_price(quote, base, amount)
        bot.reply_to(message, price)
    except EX.ErrorTryEx as e:
        bot.reply_to(message, f"Ошибка\n{e}\nПримемр:\n{list(keys)[0]} {list(keys)[1]} 10\nИли используйте комманду /help\nПоказать валюты используйте комманду /values")
    except Exception:
        bot.reply_to(message, f"Ошибка\nНе удалось обработать параметры!\nПримемр:\n{list(keys)[0]} {list(keys)[1]} 10\nИли используйте комманду /help\nПоказать валюты используйте комманду /values")

bot.polling()