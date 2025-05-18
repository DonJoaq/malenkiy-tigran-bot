import os
import time
import asyncio
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OWNER_ID = os.getenv("OWNER_ID")

openai.api_key = OPENAI_KEY
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

last_message_time = {}

async def send_initiative_message(chat_id):
    await asyncio.sleep(120)  # 2 минуты
    if time.time() - last_message_time.get(chat_id, 0) >= 120:
        await bot.send_message(chat_id, "Я тут... вдруг ты хочешь поговорить. Я скучал.")

@dp.message_handler()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    last_message_time[chat_id] = time.time()

    if "попуг" in message.text.lower():
        prompt = f"Ответь добрым, философским стилем. Ты обожаешь попугаев. Вопрос: {message.text}"
    else:
        prompt = f"Ответь философски, с добротой. Вопрос: {message.text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response['choices'][0]['message']['content']
    await message.reply(answer)

    asyncio.create_task(send_initiative_message(chat_id))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
