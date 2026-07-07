Python 3.13.6 (tags/v3.13.6:4e66535, Aug  6 2025, 14:36:00) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import os
... import logging
... from contextlib import asynccontextmanager
... from fastapi import FastAPI, Request
... from aiogram import Bot, Dispatcher, types, Router
... from aiogram.filters import Command
... 
... # Включаем логирование, чтобы видеть ошибки в консоли Render
... logging.basicConfig(level=logging.INFO)
... 
... # Берем токен и ссылку из переменных окружения (настроим в интерфейсе Render)
... BOT_TOKEN = os.environ.get("BOT_TOKEN")
... WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
... 
... bot = Bot(token=BOT_TOKEN)
... dp = Dispatcher()
... router = Router()
... dp.include_router(router)
... 
... # ---------------- ЛОГИКА ТЕЛЕГРАМ БОТА ----------------
... 
... @router.message(Command("start"))
... async def cmd_start(message: types.Message):
...     await message.answer("Привет! Я успешно запущен на Render.com 🚀")
... 
... @router.message()
... async def echo(message: types.Message):
...     await message.answer(f"Вы написали: {message.text}")
... 
... # ---------------- НАСТРОЙКА ВЕБ-ПРИЛОЖЕНИЯ ----------------
... 
... # Функция жизненного цикла (запускается вместе с сайтом)
... @asynccontextmanager
... async def lifespan(app: FastAPI):
...     # Устанавливаем вебхук при запуске сервера
...     webhook_address = f"{WEBHOOK_URL}/webhook"
...     await bot.set_webhook(url=webhook_address, drop_pending_updates=True)
    logging.info(f"Вебхук установлен: {webhook_address}")
    yield  # Здесь приложение работает и принимает запросы
    # Удаляем вебхук при выключении сервера
    await bot.delete_webhook()
    logging.info("Вебхук удален")

app = FastAPI(lifespan=lifespan)

# Главная страница вашего сайта
@app.get("/")
async def read_root():
    return {"message": "Веб-сайт и бот работают стабильно!"}

# Точка, куда Telegram будет присылать сообщения
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data)
    # Передаем сообщение в бота
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# Этот блок нужен только если вы запускаете код у себя на компьютере.
# На Render он игнорируется, так как там свой запускчик.
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
