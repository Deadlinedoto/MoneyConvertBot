import telebot
from tokentg import keys, TOKEN
from extensions import MoneyConvertor, APIException

bot = telebot.TeleBot(TOKEN)





@bot.message_handler(commands=["start", "help"])
def zapros(message: telebot.types.Message):
    text = "Здравствуйте! Чтобы начать работу с конвертатором валют, " \
           "введите в одной строке через пробел: " \
           "\n<Имя валюты, цену которой хотите узнать>" \
           "\n<Имя валюты, в которой надо узнать цену первой валюты>" \
           "\n<Количество первой валюты>." \
           "\n Чтобы узнать доступные валюты, введите команду ""/values"""
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys:
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("Вы ввели неверное число параметров")

        quote, base, amount = values
        total_base = MoneyConvertor.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} равна {total_base}"
        bot.send_message(message.chat.id, text)





bot.polling()

