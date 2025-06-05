# bot_receiver.py
import asyncio
from aiogram import Bot, Dispatcher, types
import aio_pika

API_TOKEN = '8077690095:AAG0R5hErSaeed70YS6rvf8tfSOdDo8VFBQ'
QUEUE_NAME = 'lecture_queue'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

KNOWN_USERS = {
    "username1": 7263979991,  
}

async def get_message_from_queue():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        incoming_message = await queue.get(no_ack=True)
        if incoming_message:
            return incoming_message.body.decode()
        return None

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    msg = await get_message_from_queue()
    if msg:
        username, text = msg.split("::", 1)
        await message.answer(f"📢 Викладач {username} почав віддалену пару і каже:\n{text}")
    else:
        await message.answer("⏳ Наразі немає нових повідомлень у черзі.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
