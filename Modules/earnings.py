from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message
import random
from helper import *

bp = Blueprint("Стандарт")
bp.labeler.vbml_ignore_case = True
users = "Other/users.json"
privileges = "Other/privilege.json"

# Способы получения метеоров
@bp.on.message(payload={"standard": "earning"})
async def earning(ans: Message):
    user = find("id", ans.from_id, users)
    keyboard = (
    Keyboard(inline=False)
    .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("&#9732; Разрушить метеор", {"standard": "destroy_meteor"}))
    .row()
    .add(Text("&#128220; Помощь", {"standard": "help"}))
    .row()
    .add(Text("&#9664;&#65039; Меню", {"standard": "menu"}))
    )
    await ans.answer(f"&#127918; @id{user['id']}({user['nick']}), заработки:", keyboard=keyboard)

@bp.on.message(text="разрушить метеор")
@bp.on.message(payload={"standard": "destroy_meteor"})
async def destroy_meteor(ans: Message):
    user = find("id", ans.from_id, users)
    priv = find("id", user['status'], privileges)
    add_xp(user, priv, users)
    if user['xp'] >= 1000:
        try:
            await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
        except Exception:
            print(f"У пользователя {user['nick']} закрыт личные сообщения!")
    user['balance'] += 100
    dumpjson(user, users)
    return f"&#9732; @id{ans.from_id}({user['nick']}), вы разрушили метеор. \n &#128184; Вам начислено 100 метеоров!"

# Казино
@bp.on.message(payload={"standard": "casino"})
async def info_casino(ans: Message):
    user = find("id", ans.from_id, users)
    return f"&#127920; @id{ans.from_id}({user['nick']}), чтобы сыграть в казино, введите: казино 'сумма'"

@bp.on.message(text=["казино <some>", "казик <some>"])
async def casino(ans: Message, some):
    user = find("id", ans.from_id, users)
    if user['balance'] < replace(some): 
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров!"
    if replace(some) < 500: 
        return f"&#128219; @id{ans.from_id}({user['nick']}), минимальная ставка - 500 метеоров."
    try:
        status = chance(find("id", user['status'], privileges)['chance'], x=True)
    except Exception:
        status = chance(30, x=True)
    if status['status'] == True:
        if status['bet'] == 1: 
            return f"&#128202; @id{ans.from_id}({user['nick']}), вы ничего не проиграли и не выиграли \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
        win = replace(some) * status['bet']
        priv = find("id", user['status'], privileges)
        add_xp(user, priv, users)
        if user['xp'] >= 1000:
            try:
                await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
            except Exception:
                print(f"У пользователя {user['nick']} закрыт личные сообщения!")
        user['balance'] += int(round(win))
        dumpjson(user, users)
        return f"&#128200; @id{ans.from_id}({user['nick']}), вы выиграли: {task(int(round(win)))} ({status['bet']}x) \n &#128184; Вам начислено: {task(int(round(win)))} \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    if status['bet'] == 0: 
        win = replace(some)
    else: 
        win = replace(some) * status['bet']
    user['balance'] -= int(round(win))
    dumpjson(user, users)
    return f"&#128201; @id{ans.from_id}({user['nick']}), вы проиграли: {task(int(round(win)))} ({status['bet']}x) \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"

# Кости
@bp.on.message(payload={"standard": "dice"})
async def info_dice(ans: Message):
    user = find("id", ans.from_id, users)
    return f"&#127922; @id{ans.from_id}({user['nick']}), чтобы сыграть в кости, введите: кости 'сумма'"

@bp.on.message(text=["кости <some>", "косточки <some>", "кос <som>"])
async def dice(ans: Message, some):
    user = find("id", ans.from_id, users)
    if user['balance'] < replace(some): 
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров!"
    if replace(some) < 500: 
        return f"&#128219; @id{ans.from_id}({user['nick']}), минимальная ставка - 500 метеоров."
    bot, player = random.randint(1, 6), random.randint(1, 6)
    if bot == player:
        return f"&#127922; @id{ans.from_id}({user['nick']}), у вас выпало число: {player}. \n&#127922; Выпало число у @destructionearth(бота): {bot}\n&#128433; Вы ничего не проиграли, и не выиграли!"
    if bot > player:
        user['balance'] -= int(replace(some))
        dumpjson(user, users)
        return f"&#127922; @id{ans.from_id}({user['nick']}), у вас выпало число: {player}. \n&#127922; Выпало число у @destructionearth(бота): {bot}\n&#9824;&#65039; Вы проиграли: {task(replace(some))} метеоров. \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    priv = find("id", user['status'], privileges)
    add_xp(user, priv, users)
    if user['xp'] >= 1000:
        try:
            await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
        except Exception:
            print(f"У пользователя {user['nick']} закрыт личные сообщения!")
    djackpot = random.randint(0, 100)
    if djackpot == 100:
        user['balance'] += int(replace(some) * 10)
        dumpjson(user, users)
        return f"&#127924; Джекпот!\n&#127922; @id{ans.from_id}({user['nick']}), у вас выпало число: {player}. \n&#127922; Выпало число у @destructionearth(бота): {bot}\n&#9829;&#65039; Вы выиграли: {task(replace(some) * 10)} метеоров. \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    user['balance'] += int(replace(some) * 2)
    dumpjson(user, users)
    return f"&#127922; @id{ans.from_id}({user['nick']}), у вас выпало число: {player}. \n&#127922; Выпало число у @destructionearth(бота): {bot}\n&#9829;&#65039; Вы выиграли: {task(replace(some) * 2)} метеоров. \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"