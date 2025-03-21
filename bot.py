import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
import aiohttp

# 🔹 ЗАМЕНИ на свой токен!
TOKEN = "7866480501:AAEAqEtSoVfM-xj_y9-oT-_MNCsq-rmQeLQ"

# 🔹 Укажи URL своего бекенда (локально или на сервере)
BALANCE_API = "http://localhost:8000/balance/"  # Или укажи реальный хостинг

# 🔹 Ссылка на казино-мини-приложение
CASINO_URL = "https://casino-webapp-1vc0j34xk-wsxs-projects-76072096.vercel.app"

# 🔹 Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# 🔹 Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# 🔹 Команда /start
@router.message(Command("start"))
async def start(message: types.Message):
    text = (
        "🎰 Добро пожаловать в Казино!\n\n"
        "💰 Проверь свой баланс: /balance\n"
        "🎮 Играть в казино: [НАЖМИ СЮДА]({})"
    ).format(CASINO_URL)
    
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

# 🔹 Команда /balance
@router.message(Command("balance"))
async def get_balance(message: types.Message):
    user_id = message.from_user.id
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BALANCE_API}{user_id}") as response:
            if response.status == 200:
                data = await response.json()
                balance = data.get("balance", 0)
                await message.answer(f"💰 Ваш баланс: {balance} монет")
            else:
                await message.answer("⚠ Ошибка при получении баланса. Проверь API.")

# 🔹 Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
