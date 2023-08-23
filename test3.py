import re
from PIL import Image, ImageDraw, ImageFont

def clean_string(text):
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)  # Очистка строки от неподдерживаемых UTF-символов
    return cleaned_text

def write_text_on_image(image_path, text):
    image = Image.open(image_path)  # Открытие изображения
    draw = ImageDraw.Draw(image)  # Создание объекта для рисования на изображении
    font = ImageFont.truetype("Nunito-Regular.ttf", 40)  # Загрузка шрифта Nunito-Regular.ttf размером 20
    cleaned_text = clean_string(text)  # Очистка текста от неподдерживаемых символов
    draw.text((10, 10), cleaned_text, font=font, fill=(0, 0, 0))  # Нанесение текста на изображение с помощью указанного шрифта и цвета
    image.save("output_image.jpg")  # Сохранение измененного изображения

text = "Hi, botmakers! 👋😊"  # Задание текста
image_path = "image.jpg"  # Путь к исходному изображению
write_text_on_image(image_path, text)  # Вызов функции для добавления текста на изображение