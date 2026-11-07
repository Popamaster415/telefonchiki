import random
import json
from pyrogram import Client, filters
import config
import keyboards
import datetime
from Stablecog_AI import generate
from pyrogram.types import ForceReply
bot=Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name='Бульбаш'
)
@bot.on_message(filters.command('image'))
async def image(bot,message):
    if len (message.text.split()) >1:
        query=message.text.replace('/image','')
        await message.reply_text(f'Генерирую изображение по запросу "{query}",подождите немного...')
        images=generate(query)

        if images:
            await bot.send_photo(message.chat.id, images[0],reply_to_message_id=message.id)
        else:
            await message.reply_text('Возникла ошибка, попробуйте еще раз',reply_to_message_id=message.id)

    else:
        await message.reply_text('Введите запрос в формате: /image маленький котик')

def button_filter(button):
    async def func(_,__, msg):
        return msg.text==button.text
    return filters.create(func,'ButtonFilter',button=button)
@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply('Добро пожаловать,чем хочешь заняться?',
                        reply_markup=keyboards.kb_main)
    print(message.from_user.username)
    with open('users.json','r') as file:
        users=json.load(file)
    if str(message.from_user.username) not in users.keys():
        users[message.from_user.username]=100
        with open('users.json','w') as file:
            json.dump(users,file)

@bot.on_message(filters.command('info')|button_filter(keyboards.btn_info))
async def info(bot,message):
    await message.reply('Привет! Тут описание что может этот бот и список команд')

@bot.on_message(filters.command('time')|button_filter(keyboards.btn_time))
async def time(bot, message):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    await message.reply(current_time)

@bot.on_message(filters.command('games') | button_filter(keyboards.btn_games))
async def games(bot, message):
    await message.reply('Выбери игру',reply_markup=keyboards.kb_games)

query_text='Введите запрос для генерации изображения'
@bot.on_message (button_filter(keyboards.btn_generate))
async def image_command(bot, message):
    await message.reply(query_text,reply_markup=ForceReply(True))
@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text==query_text:
        query=message.text
        await message.reply_text(f'Генерирую изображение по запросу **{query}**.Ожидание около минуты')
        images = generate(query)

        if images:
            await bot.send_photo(message.chat.id, images[0], reply_to_message_id=message.id)
        else:
            await message.reply_text('Возникла ошибка, попробуйте еще раз', reply_to_message_id=message.id)

@bot.on_message(filters.command('game') | button_filter(keyboards.btn_rps))
async def game(bot, message):
    await message.reply('Выберите предмет',reply_markup=keyboards.kb_rps)
    with open('users.json','r') as file:
        users=json.load(file)
    if users [str(message.from_user.username)]>=10:
        await message.reply('Твой ход', reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f'Не хватает средств, на твоем счету {users[str(message.from_user.username)]}.Минимальная сумма для игры-10')
@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_paper) |
                button_filter(keyboards.btn_scissors))
async def choice_rps(bot,message):
    with open('users.json','r') as file:
        users=json.load(file)
    rock=keyboards.btn_rock.text
    scissors=keyboards.btn_scissors.text
    paper=keyboards.btn_paper.text
    user=message.text
    pc=random.choice([rock,scissors,paper])

    if user==pc:
        await message.reply('Ничья')
    elif((user ==rock and pc ==scissors) or
         (user == scissors and pc == paper) or
         (user == paper and pc == rock)):
        await message.reply(f'Ты выйграл.Бот выбрал {pc}',
                            reply_markup=keyboards.kb_games)
        users[str(message.from_user.username)] += 10
    else:
        await message.reply(f'Ты проиграл.Бот выбрал {pc}',
                            reply_markup=keyboards.kb_games)
        users[str(message.from_user.username)] -=10
    with open('users.json','w') as file:
        json.dump(users, file)

# @bot.on_message(filters.command('rating') | button_filter(keyboards.btn_profile))
# async def rating_handler(client,mwssage):
#     with open('users.json','r') as file:
#         pass

@bot.on_message(filters.command('profile') | button_filter(keyboards.btn_profile))
async def profile (bot, message):
    with open('users.json','r') as file:
        data=json.load(file)
    text = "🏆 Рейтинг игроков:\n\n"

    for i, (user, coins) in enumerate(
        reversed(sorted(data.items(), key=lambda x: (x[1], x[0]))), start=1
    ):
        text += f"{i}. {user} - {coins}\n"

    await message.reply(text, reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('back') | button_filter(keyboards.btn_back))
async def back (bot, message):
    await message.reply('Возврат в главное меню', reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('quest') | button_filter(keyboards.btn_quest))
async def kvest(bot,message):
    await message.reply_text('Хотите ли вы отправится в увлекательеное путешествие,полное приключений и загадок?',
                             reply_markup=keyboards.inline_kb_start_quest)
@bot.on_callback_query()
async def handle_query(bot,query):
    await query.message.delete()
    if query.data=='start_quest':
        await bot.answer_callback_query(query.id,text='Добро пожаловать в квест под названием Поиски Затерянного Сокровища!',show_alert=True)
        await query.message.reply_text('Ты стоишь перед двумя дверьми.Какую из них ты выберешь?',
                                       reply_markup=keyboards.inline_kb_choice_door)
    elif query.data=='left_door':
        await query.message.reply_text('Ты входишь в комнату и видишь злого дракона!У тебя есть два варианта:',
                                       reply_markup=keyboards.inline_kb_left_door)
    elif query.data=='dragon':
        await bot.answer_callback_query(query.id,text='Ты сражаешься с драконом, но он оказывается слишком сильным.Ты погибаешь',
                                        show_alert=True)
    elif query.data=='run':
        await bot.answer_callback_query(query.id,text='Ты пытаешься убежать,но дракон догоняет тебя и съедает',
                                        show_alert=True)
    elif query.data == 'right_door':
        await query.message.reply_text('Ты входишь в комнату наполненную сокровищами!Тебе нужно выбрать только одно сокровище:',
                                       reply_markup=keyboards.inline_kb_right_door)
    elif query.data == 'gold_crown':
        await bot.answer_callback_query(query.id, text='Ты берешь золотую корону и выходишь из комнаты.Поздравляю ты выйграл игру',
                                        show_alert=True)
    elif query.data == 'silver_dagger':
        await bot.answer_callback_query(query.id,text='Ты берешь серебряный кинжал и выходишь из комнаты.К сожалению,кинжал ничего не стоит',
                                        show_alert=True)
    elif query.data == 'old_book':
        await bot.answer_callback_query(query.id,text='Ты берешь старую книгу и выходишь из комнаты.Книга оказывается магической!Ты открываешь страницу и исчезаешь',
                                        show_alert=True)

@bot.on_message()
async def echo(bot, message):
    if message.text.lower() =='привет':
        await message.reply('Привет)')
    elif message.text.lower() == 'пока':
        await message.reply('Пока(')
    else:
        await message.reply(f'Ты написал:{message.text}')

bot.run()
