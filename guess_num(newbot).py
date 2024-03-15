from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random

token_bot = 'bottoken'

# Создаем объекты бота и диспетчера
bot = Bot(token_bot)
dp = Dispatcher()

attemp = 5

users = {}


# Функция возвращающая случайное целое число от 1 до 100


def get_random_num() -> int:
    return random.randint(1,  100)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def proccess_start_command(mesasge: Message):
    await mesasge.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправитье команду /help'
    )
    if mesasge.from_user.id not in users:
        users[mesasge.from_user.id] = {
            'in_game': False,
            'secret_num': None,
            'attemp': None,
            'total_games': 0,
            'wins': 0
        }


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def proccess_help_command(mesasge: Message):
    await mesasge.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {attemp} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def proccess_stat_command(message: Message):
    await message.answer(
        f"Всего сыгранно игр - {users[message.from_user.id]['total_games']}\n"
        f"Игр выигранно - {users[message.from_user.id]['wins']}"
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def proccess_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игруf
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def proccess_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_num'] = get_random_num()
        users[message.from_user.id]['attemp'] = attemp
        await message.answer(
            'Ура!\nЯ загадал число от 1 до 100, '
            'поробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def procces_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def proccess_num(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_num']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['wins'] += 1
            users[message.from_user.id]['total_games'] += 1
            await message.answer("Ура!!! Вы угадали число\nМожет сыграем еше?")
        elif int(message.text) > users[message.from_user.id]['secret_num']:
            users[message.from_user.id]['attemp'] -= 1
            await message.answer("Мое число меньше")
        elif int(message.text) < users[message.from_user.id]['secret_num']:
            users[message.from_user.id]['attemp'] -= 1
            await message.answer("Мое число больше")

        if users[message.from_user.id]['attemp'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f"К сожалению у вас больше не осталось попыток. "
                f"Вы проиграли :(\n"
                f"Мое число было {users[message.from_user.id]['secret_num']}.\n"
                f"Давайте сыграем еще раз?"
            )
    else:
        await message.answer("Мы еще не начали нашу игру\nДавайте сыграем?")


@dp.message()
async def proccess_other_text(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer("Мы с вами играем в игру\nПожалуйста присылайте только\nчисла от 1 до 100")
    else:
        await message.answer("Я умею только играть в эту игру.\nДавайте сыграем?")


if __name__ == '__main__':
    dp.run_polling(bot)
