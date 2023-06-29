import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды!')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "туман \U0001F32B"
    }

    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric"%(message.text, open_weather_token)
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply("*** " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + " ***" + "\nПогода в городе: %s"%city + "\nТемпература: %s"%cur_weather +  "C°,  "  + "%s"%wd + "\nВлажность: %s"%humidity + "%" + "\nДавление: %s"%pressure + "мм.рт.ст" + "\nСкорость ветра: %s"%wind + "м/с" + "\nВосход солнца: %s"%sunrise_timestamp + "\nЗакат: %s"%sunset_timestamp + "\nХорошего дня!")

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)