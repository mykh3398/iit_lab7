# bot_sender.py
import asyncio
from aiogram import Bot, Dispatcher, types
import aio_pika

API_TOKEN = '8011258897:AAEjIi1rC5VZVmPqK5CgcdbkIG6g6JifBP8'
QUEUE_NAME = 'lecture_queue'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def send_to_queue(message_text: str, sender_id: int, sender_username: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        message = f"{sender_username or sender_id}::{message_text}"
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=QUEUE_NAME,
        )

@dp.message_handler(commands=['lecture'])
async def handle_lecture(message: types.Message):
    text = "Пара щойно почалась! Підключайтесь за посиланням: https://zoom.us/j/123456789"
    await send_to_queue(text, message.from_user.id, message.from_user.username)
    await message.reply("📨 Повідомлення про початок пари надіслано в чергу.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
