import os
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from openai import OpenAI


# Логи помилок
logging.basicConfig(level=logging.INFO)

# Завантаження .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Перевірка ключів
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не знайдено")


# Telegram
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


# OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)


SYSTEM_PROMPT = """
Ти AI чат-бот підтримки користувачів.

Твоя спеціалізація:

- програмування
- Python
- SQL
- бази даних
- мережеві технології
- кібербезпека
- операційні системи
- комп'ютерні технології
- IT інфраструктура

Якщо користувач питає НЕ про IT —
ввічливо повідом,
що бот працює лише з IT тематикою.
"""


@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "Привіт 👋\n\n"
        "Я AI чат-бот підтримки у сфері IT.\n\n"
        "Став питання."
    )


@dp.message(Command("help"))
async def help_command(message: Message):

    await message.answer(
        "Приклади:\n\n"
        "• Що таке Python?\n"
        "• Що таке DNS?\n"
        "• Як працює SQL?\n"
        "• Що таке Docker?"
    )


@dp.message()
async def ai_answer(message: Message):

    try:

        user_text = message.text

        wait_message = await message.answer(
            "Обробляю запит..."
        )

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": user_text
                }

            ],

            temperature=0.5

        )

        answer = response.choices[0].message.content

        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=wait_message.message_id
        )

        await message.answer(answer)

    except Exception as e:

        print(e)

        logging.error(e)

        await message.answer(

            f"Помилка:\n{str(e)}"

        )


async def main():

    print("Бот запущений")

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())