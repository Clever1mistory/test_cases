import asyncio
import aiogram
from aiogram import types
import bleach

# Создание экземпляра бота и диспетчера
bot = aiogram.Bot(token='TOKEN')
dp = aiogram.Dispatcher(bot)

# Обработчик входящих сообщений с типом "Document"
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    if message.document.mime_type == 'text/plain':
        doc = await bot.get_file(message.document.file_id)
        file = await bot.download_file(doc.file_path)
        text = bleach.clean(file.read().decode('utf-8'), tags=[], strip=True)
        await message.reply(text)

# Обработчик команды "/profile"
@dp.message_handler(commands=['profile'])
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    profile_photo = types.InputFile("./profile_photo.png")

    # Создание кнопки
    button = types.KeyboardButton(text="/profile")
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(button)

    await message.reply_photo(photo=profile_photo, caption=f"Username: {user_name}\nUser ID: "
                                                           f"{user_id}", reply_markup=keyboard)

# Обработчик команды "/start"
@dp.message_handler(commands=['start'])
async def show_start_menu(message: types.Message):
    # Создание кнопки
    button = types.KeyboardButton(text="/profile")
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(button)

    await message.reply("Отправьте текстовый файл или нажмите на кнопку /profile", reply_markup=keyboard)

# Запуск бота на выполнение
if __name__ == '__main__':
    asyncio.run(aiogram.executor.start_polling(dp))