from pyrogram.filters import inline_keyboard
from pyrogram.types import KeyboardButton,InlineKeyboardButton
from pyrogram.types import ReplyKeyboardMarkup,InlineKeyboardMarkup
from pyrogram import emoji

btn_generate=KeyboardButton(f'{emoji.FRAMED_PICTURE} генерация изображения')
btn_info=KeyboardButton(f'{emoji.INFORMATION} Инфо')
btn_games=KeyboardButton(f'{emoji.VIDEO_GAME} Игры')
btn_profile=KeyboardButton(f'{emoji.PERSON }  Рейтинг игроков')
btn_rps=KeyboardButton(f'{emoji.PLAY_BUTTON } Камень,ножницы и бумага')
btn_quest=KeyboardButton(f'{emoji.CITYSCAPE_AT_DUSK } Квест')
btn_back=KeyboardButton(f'{emoji.BACK_ARROW  } Назад')
btn_time=KeyboardButton(f'{emoji.TIMER_CLOCK  } Время')
btn_rock=KeyboardButton(f'{emoji.ROCK} камень')
btn_scissors=KeyboardButton(f'{emoji.SCISSORS } ножницы')
btn_paper=KeyboardButton(f'{emoji.NOTEBOOK } бумага')
inline_kb_start_quest=InlineKeyboardMarkup([[InlineKeyboardButton('Пройти квест',
                                                                callback_data='start_quest')]])
kb_main=ReplyKeyboardMarkup(
    keyboard=[
    [btn_info, btn_games],
    [btn_profile,btn_time],
        [btn_generate]
        ],
   resize_keyboard=True
)
kb_games=ReplyKeyboardMarkup(
    keyboard=[
    [btn_rps, ],
    [btn_quest, btn_back,],
        ],
   resize_keyboard=True
)
kb_rps=ReplyKeyboardMarkup(
    keyboard=[
    [btn_scissors,btn_rock,btn_paper ],
    [btn_back,],
        ],
   resize_keyboard=True
)

inline_kb_choice_door=InlineKeyboardMarkup([
    [InlineKeyboardButton('🚪⬅️левая дверь',callback_data='left_door')],
    [InlineKeyboardButton('️️ ➡️🚪правая дверь',callback_data='right_door')]
])
inline_kb_left_door=InlineKeyboardMarkup([
    [InlineKeyboardButton('🐲Сражаться с драконом',callback_data='dragon')],
    [InlineKeyboardButton('️️🏃Попытаться убежать',callback_data='run')]
])

inline_kb_right_door=InlineKeyboardMarkup([
    [InlineKeyboardButton('👑Золотая корона',callback_data='gold_crown')],
    [InlineKeyboardButton('️️🗡️Серебряный кинжал',callback_data='silver_dagger')],
    [InlineKeyboardButton('📕Старая книга',callback_data='old_book')]
])
