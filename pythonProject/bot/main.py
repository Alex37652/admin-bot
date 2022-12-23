from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from random import choice
from dotenv import load_dotenv
from os import getenv

abusive_language = []

stickers_id = ['CAACAgIAAx0CZJPBwwADM2OghcCiq_HKUYVe6gbii0zSiysaAAInGAACl3nhS9YBFhLexd9PLAQ',
               'CAACAgIAAx0CZJPBwwADNGOghcIwSojgT5wGk9L_PZRhYGoMAAIRFAACoAAB6EuHKd82dqZdoSwE',
               'CAACAgIAAx0CZJPBwwADNWOghcSQXrpK7WwCRQi5TxbR4X40AALnEgAC75LoS9j0h9FeRn4sLAQ',
               'CAACAgIAAx0CZJPBwwADNmOghcYZw-PVKL6iG24Usd3HNljfAAK2EwACPzfpS94s_xOxQLUvLAQ',
               'CAACAgIAAx0CZJPBwwADN2Oghcha5CcvWeGxYqGJX1EfTnm3AAI8FQACBabgSyGSjAYhPJQSLAQ',
               'CAACAgIAAx0CZJPBwwADOGOghcqSHcXxrpFHYXH6F4oriV5vAALXGAACbibhSwVjLcKY6_yrLAQ',
               'CAACAgIAAx0CZJPBwwADOWOghc0e_Aifef_zuEXdPC-pKbGJAAIuEAACk3npS9OR9m6tWiW_LAQ',
               'CAACAgIAAx0CZJPBwwADOmOghc99aTpIkGYuhNuakD9mJ1faAAIoFgACLzHhS-wCebmFOMQdLAQ',
               'CAACAgIAAx0CZJPBwwADO2OghdEWUx9mDweF2y8WO9_0JvcPAALOFgAC6S7hS3dAtqlRuoq-LAQ',
               'CAACAgIAAx0CZJPBwwADPGOghdPvC2FRtIIETr5jcvg3VpN5AALAFwAC-cfhSziGjHtF4Ui6LAQ',
               'CAACAgIAAx0CZJPBwwADPWOghdVa_56vHyBHSa2BTFzjMJ0qAAJJEgAC1TzpSxnef47xiPyoLAQ',
               'CAACAgIAAx0CZJPBwwADPmOghde-oV4PIcZsvhw5WxKoVk2oAALdFwACrnHhS2fqq7fGCapBLAQ',
               'CAACAgIAAx0CZJPBwwADP2Oghdpzu4PqFHx_UmJWLpGobPUOAALXGAACrbbhS6rrx1LlidAwLAQ',
               'CAACAgIAAx0CZJPBwwADQGOghdvYHSLY967w83TTex3-rTa2AAIeFQACpdPpS1J1vLiRVUtCLAQ',
               'CAACAgIAAx0CZJPBwwADQWOghd1Iw-1WqNw7TxNWd8bZGIhtAAIHEwACA0rhS_rUUiQdLqIWLAQ',
               'CAACAgIAAx0CZJPBwwADQmOgheDZaE46PhrAkLrBPkRdoGQBAAL4EQACg8XpS9U9AaLTuTeNLAQ',
               'CAACAgIAAx0CZJPBwwADQ2OgheLdb9Ce6bHeLb11wSaytfL_AALcFAACdZ_gS0iNptUI0b4-LAQ',
               'CAACAgIAAx0CZJPBwwADRGOgheTvD-8tCHyVF7rfnDyztiLpAAJuFAACSjvhS687bMy4TZ5QLAQ',
               'CAACAgIAAx0CZJPBwwADRWOgheZPJGwGEsM-8oRTN7xGrB8YAAKQGQACp-lBSktAYLmUx35ZLAQ',
               'CAACAgIAAx0CZJPBwwADRmOghemECkYm2I2EznHdOAABcrt3YQACXhUAAmXa6EtTb2HwOntzoSwE',
               'CAACAgIAAx0CZJPBwwADR2Oghe3WQy_kjTFpfSjkVckTy0gsAAI-FgACJHY5SE4XzS2f-3n0LAQ',
               'CAACAgIAAx0CZJPBwwADSGOghe9c579jGgqlFrmBC4ij503nAAL3FAADlTlKYY4rWKgEsY0sBA',
               'CAACAgIAAx0CZJPBwwADSWOghfUV45JoKXQ5nvcZp_OpGsVGAAKvGQACrkY4SpkGEBBRGcoMLAQ',
               'CAACAgIAAx0CZJPBwwADSmOghfdwQbhQw3A884YAAUkspz_zVAACmhUAAhjCOUoQthLkmEXldSwE',
               'CAACAgIAAx0CZJPBwwADS2OghfpcsUdWpW50svw-BDrpZ9kUAAIHHwACjQUxSoJZKJsmpvtmLAQ',
               'CAACAgIAAx0CZJPBwwADTGOghgEn6XWfy3gjBujoPBHU361XAAI_EwAC2XA4SlLD-vbK33zyLAQ',
               'CAACAgIAAx0CZJPBwwADTWOghgOOWDDA1PYJu4c8yhyGaMOJAALPFAACG-k4SuVyJCvNuaI7LAQ',
               'CAACAgIAAx0CZJPBwwADTmOghgXW9xGcSQQd4urXyQ7nPdYeAAK_FwACSzw4So8dIG4TkRYYLAQ',
               'CAACAgIAAx0CZJPBwwADT2OghghkF6rx50rOhjUvQEeET0YcAAJBFQACMvo5SqL0sTBxij-cLAQ',
               'CAACAgIAAx0CZJPBwwADUGOghgok4LFNzuMoPHAyqnULWiaRAAI1GgACezswSvdOthGjsG3TLAQ',
               'CAACAgIAAx0CZJPBwwADUWOghgzcvAAB6TrdjbmBU7jLP2ZlBAACZRUAAjIxOUpRvz3227nqwSwE',
               'CAACAgIAAx0CZJPBwwADUmOghg6HQ9c_XWBB78_5Owjd4MtYAAI7EgACuGI4Sv1rAtq79edlLAQ',
               'CAACAgIAAx0CZJPBwwADU2OghhDcclIZvhD3Ih9vP_L6QHqkAAKHGgACvU04Sr2w-On55T4JLAQ',
               'CAACAgIAAx0CZJPBwwADVGOghhN8wvZz3DtRN0fUScRf6jU0AAJpFwACqck5SgG7zgHbWXLqLAQ',
               'CAACAgIAAx0CZJPBwwADVWOghhWCF-8YyqTAmBwmPoJ4uaGCAAILGAACpxY4StlHxyfnO05tLAQ',
               'CAACAgIAAx0CZJPBwwADVmOghhdCjpqPn6RfztlwOkOxcKwzAAJZFQACOU04Srvlg3GMVyg3LAQ',
               'CAACAgIAAx0CZJPBwwADV2OghhkPQcHBZmSXIam1kLXRdkoDAAKqGwACX_vJSlb3OhM_h9gfLAQ',
               'CAACAgIAAx0CZJPBwwADWGOghhwTXMU2JeXd6dmj3NvPP8grAAJaHAACmNPJSkQEUsjM41jkLAQ',
               'CAACAgIAAx0CZJPBwwADWWOghiB_dVji-9w9deTRwj65gErIAAIbGgACSDPRSvTbxyRUICGILAQ',
               'CAACAgIAAx0CZJPBwwADWmOghiLZeMauwwSnYIkQu_UsjTcxAAIaGgACqVPQSiv_bdi48XUgLAQ',
               'CAACAgIAAx0CZJPBwwADW2OghiSl5H1ggZKPEtvVZwOujNYmAALpHgACYCfJSh6dAg4QNezBLAQ',
               'CAACAgIAAx0CZJPBwwADXGOghiYzRlQKVMgAAfgOZbAj9q56mgACrx4AAq0g0EoW-WsFcEaYfiwE',
               'CAACAgIAAx0CZJPBwwADXWOghilELAFpv1LEIAQfv6DQ6uMjAAISGgACVojJSkT7frv_7czuLAQ',
               'CAACAgIAAx0CZJPBwwADXmOghitbTxyWgZ-JA-ZwcQAB8GbJRgAClBsAApngyEp67FOO_tH2zSwE',
               'CAACAgIAAx0CZJPBwwADX2Oghi1yr5iIU2jVh8WOAZCySUPKAAJKHwAC6azRSjaMxgQHS1a9LAQ',
               'CAACAgIAAx0CZJPBwwADYGOghi-hfYWFBfFvIecfy_lGMa34AAKRHAACGCrQSkICTZ997DZvLAQ',
               'CAACAgIAAx0CZJPBwwADYWOghjHi9Vmq8SlnkVVMSwV33pfMAAJFGgACmFTQSn1_1emWhYFgLAQ',
               'CAACAgIAAx0CZJPBwwADYmOghjOf9Yxb74XEzoctgylSeNAhAALLHQACwJvJSlMF1YbBiMB4LAQ',
               'CAACAgIAAx0CZJPBwwADY2OghjSOUXG65rHceJarpOPosE8sAAJGIAACRFvIStYbmacjFL5oLAQ',
               'CAACAgIAAx0CZJPBwwADZGOghjZ5z2HKetc2Hux5xtL81bA5AAJGFwACnxTRSqLcP2yzOB0HLAQ']

load_dotenv('./token.env')

TOKEN = getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

data = dict()


class FSMCommands(StatesGroup):
    ban_user = State()
    unban_user = State()
    new_admin = State()
    add_word = State()


async def check_root(message: types.Message):
    for admin in (await bot.get_chat_administrators(chat_id=message.chat.id)):
        if admin["user"]["id"] == message.from_user.id:
            return True
    return False


def username_checker(chat_id: int, input_username: str):
    username = input_username
    if input_username[0] == '@':
        username = input_username[1:len(input_username)]
    if username in data[chat_id].keys():
        return data[chat_id][username]
    return 'no such user'


@dp.message_handler(commands="start")
async def command_start(message: types.Message):
    data[message.chat.id] = data.get(message.chat.id, dict())
    await bot.set_my_commands(
        [BotCommand("ban", 'ban user'),
         BotCommand('bot_leave_chat', 'кикнуть бота'),
         BotCommand('pinned_messag', 'закрепить сообщение'),
         BotCommand('clear_pinned_messages', 'очистить закрепы'),
         BotCommand('set_new_admin', 'сделать нового админа'),
         BotCommand('start', 'запустить бота'),
         BotCommand('unban', 'разбанить юзера'),
         BotCommand('send_random_sticker', 'отправить стикер с хасбиком'),
         BotCommand('add_abusive_word', 'добавить слово в список забанненых слов')])
    await message.answer("Всем привет, я АдминЧатБот")


@dp.message_handler(commands="send_random_sticker")
async def send_sticker(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    await message.answer_sticker(choice(stickers_id))


@dp.message_handler(commands="add_abusive_word")
async def add_abusive_word(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    await FSMCommands.add_word.set()
    await message.answer("Напишите слово, которое надо забанить")


@dp.message_handler(state=FSMCommands.add_word)
async def add_word(message: types.Message, state: FSMContext):
    abusive_language.append(message.text)
    await message.answer("Слово добавлено")
    await state.finish()


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def some_handler(message: types.Message):
    data[message.chat.id] = data.get(message.chat.id, dict())
    for user in message.new_chat_members:
        data[message.chat.id][user["username"]] = user['id']


@dp.message_handler(commands="ban")
async def get_user_id_for_ban(message: types.Message):
    data[message.chat.id] = data.get(message.chat.id, dict())
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    if await check_root(message):
        await FSMCommands.ban_user.set()
        await message.answer("Напишите имя пользователя")
    else:
        await message.answer("Права есть только у администраторов")


@dp.message_handler(state=FSMCommands.ban_user)
async def ban_user(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer("Процесс бана отменен")
        await state.finish()
        return
    result = username_checker(message.chat.id, message.text)
    if result == 'no such user':
        await message.answer("В чате нет такого пользователя")
        await state.finish()
    else:
        await bot.ban_chat_member(chat_id=message.chat.id,
                                  user_id=result)
        await message.answer("Пользователь забанен")
        await state.finish()


@dp.message_handler(commands="unban")
async def get_user_id_for_unban(message: types.Message):
    data[message.chat.id] = data.get(message.chat.id, dict())
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    if await check_root(message):
        await FSMCommands.unban_user.set()
        await message.answer("Напишите его имя пользователя")
    else:
        await message.answer("Права есть только у администраторов")


@dp.message_handler(state=FSMCommands.unban_user)
async def unban_user(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer("Процесс разбана отменен")
        await state.finish()
        return
    result = username_checker(message.chat.id, message.text)
    if result == 'no such user':
        await message.answer("В чате нет такого пользователя")
        await state.finish()
    else:
        await bot.unban_chat_member(chat_id=message.chat.id,
                                    user_id=result)
        await message.answer("Пользователь разбанен")
        await state.finish()


@dp.message_handler(commands="bot_leave_chat")
async def leave_chat(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    if await check_root(message):
        await message.answer("I'll be back!")
        await bot.leave_chat(chat_id=message.chat.id)
    else:
        await message.answer("Права есть только у администраторов")


@dp.message_handler(commands="set_new_admin")
async def get_user_id_for_new_admin(message: types.Message):
    data[message.chat.id] = data.get(message.chat.id, dict())
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    if await check_root(message):
        await FSMCommands.new_admin.set()
        await message.answer("Напишите имя пользователя")
    else:
        await message.answer("Права есть только у администраторов")


@dp.message_handler(state=FSMCommands.new_admin)
async def set_admin(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer("Процесс добавления нового админа отменен")
        await state.finish()
        return
    result = username_checker(message.chat.id, message.text)
    if result == 'no such user':
        await message.answer("В чате нет такого пользователя")
        await state.finish()
    else:
        if check_root(message):
            await message.answer("Пользователь уже админ")
            await state.finish()
            return
        await bot.promote_chat_member(chat_id=message.chat.id,
                                      user_id=result,
                                      can_manage_chat=True,
                                      can_change_info=True,
                                      can_delete_messages=True,
                                      can_manage_video_chats=True,
                                      can_promote_members=True,
                                      can_pin_messages=True,
                                      can_edit_messages=True,
                                      can_post_messages=True,
                                      can_restrict_members=True,
                                      can_invite_users=True)
        await message.answer("Новый админ добавлен")
        await state.finish()


@dp.message_handler(commands='pinned_messag')
async def pin(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    if message.from_user.id != message.chat.id:
        if await check_root(message):
            try:
                await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
            except:
                await message.answer('Напишите /pin в виде ответа на сообщение, которое хотите закрепить')


@dp.message_handler(commands='clear_pinned_messages')
async def unpin(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer('Я создан для чатов, не пиши мне в личку пожалуйста')
        return
    if await check_root(message):
        await bot.unpin_all_chat_messages(message.chat.id)
        await message.answer("Все закрепы очищены")
    else:
        await message.answer("Права есть только у администраторов")


@dp.message_handler()
async def collect_all_messages(message: types.Message):
    if message.from_user.id != bot.id:
        data[message.chat.id] = data.get(message.chat.id, dict())
        data[message.chat.id][message.from_user.username] = message.from_user.id
    for word in message.text.split():
        if word in abusive_language:
            await bot.delete_message(message.chat.id, message.message_id)
            return


executor.start_polling(dp, skip_updates=True)
