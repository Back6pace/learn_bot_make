from typing import Any
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, BaseFilter

token_bot = '7039241340:AAGkOk1b5XgaktCwla3eEJ43pJse5KDYHg4'

# Создаем объекты бота и диспетчера
bot = Bot(token_bot)
dp = Dispatcher()

# Проверка, являеться ли пользователь администратором бота, для того чтобы можно было выполнять различные функиции доступные только администратором
admins: list[int] = [6305517305]


class IsAdmin(BaseFilter):
    def __init__(self, admins: list[int]) -> None:
        self.admins = admins

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins


# Поиск чисел в сообщении с помощью класса
class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        # Разрезаем сообщение по пробелам, нормализуем каждую часть, удаляя
        # лишние знаки препинания и невидимые символы, проверяем на то, что
        # в таких словах только цифры, приводим к целым числам
        # и добавляем их в список
        for el in message.text.split():
            normalized_el = el.replace('.', '').replace(',', '').strip()
            if normalized_el.isdigit():
                numbers.append(int(normalized_el))
        # Если в списке есть числа - возвращаем словарь со списком чисел по ключу 'numbers'
        if numbers:
            return {'numbers': numbers}
        return False


@dp.message(F.text.lower().startswith('найди числа'), NumbersInMessage(), IsAdmin(admins))
async def proccess_if_num(message: Message, numbers: list[int]):
    await message.answer(text=f"Нашел: {', '.join(str(num) for num in numbers)}")


@dp.message(F.text.lower().startswith('найди числа'))
async def proccess_no_num(message: Message):
    await message.answer("Ничего не нашел :(")


if __name__ == '__main__':
    dp.run_polling(bot)
