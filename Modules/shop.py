from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message
from helper import *

bp = Blueprint("Стандарт")
bp.labeler.vbml_ignore_case = True
users = "Other/users.json"
privileges = "Other/privilege.json"
starships = 'Other/starship.json'

# Весь магазин
@bp.on.message(text=["магазин", "магаз", "shop"])
@bp.on.message(payload={"standard": "shop"})
async def shop(ans: Message):
    user = find("id", ans.from_id, users)
    keyboard, status, starsipss = "", f"&#127895; Статусы:", f"\n&#128640; Звездолеты:"
    num, nums = 49, 49
    for i in loadjson(privileges):
        status += f"\n&#{num};&#8419; {i['emoji']} {i['name']} статус \n⠀&#9881; Номер товара: {i['id']} \n⠀&#128179; Стоимость: {task(i['price'])} \n⠀&#8986; Срок: {i['status_time']}\n"
        num += 1
    for i in loadjson(starships):
        starsipss += f"\n&#{nums};&#8419; {i['emoji']} {i['name']} \n⠀&#9881; Номер товара: {i['id']} \n⠀&#9889;&#65039; Дальность: {task(i['range'])} А.Е. \n⠀&#9876; Урон: {task(i['damage'])} \n⠀&#128179; Стоимость: {task(i['price'])}\n"
        nums += 1
    if user['buttons'] == True:
        keyboard = (
        Keyboard(inline=False)
        .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("&#127941; Топ", {"standard": "top"}))
        .add(Text("&#128737; Клан", {"standard": "clan"}))
        .add(Text("&#128301; Локации", {"standard": "locations"}))
        .row()
        .add(Text("&#128377; Игры", {"standard": "game"}))
        .add(Text("&#128182; Заработок", {"standard": "earning"}))
        .row()
        .add(Text("&#128220; Помощь", {"standard": "help"}))
        .row()
        .add(Text("&#9664;&#65039; Меню", {"standard": "menu"}))
        )
    await ans.answer(f"&#128220; @id{ans.from_id}({user['nick']}), вот мои товары:\n\n" + status + starsipss + f"\n\n Вы находитесь на 1 странице из 1. Напишите: магазин 'номер страницы' \n &#128722; Чтобы купить товар, напишите: купить 'категория' 'номер товара' \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров.",  keyboard=keyboard)

# Покупка
@bp.on.message(text="купить <category> <id>")
async def buy_shops(ans: Message, category, id):
    user = find("id", ans.from_id, users)
    if int(category) == 1:
        privilege = find("id", int(id), privileges)
        if not privilege:
            return f"&#128219; @id{ans.from_id}({user['nick']}), такого товара не существует!"
        if user['balance'] < privilege['price']:
            return f"&#128219; @id{ans.from_id}({user['nick']}), у вас не хватает метеоров!\n&#127895; Стоимость {privilege['name']} статуса: {task(privilege['price'])} метеоров\n&#9732; Ваш текущий баланс: {task(user['balance'])} метеоров."
        if user['status'] == privilege['id']:
            return f"&#128219; @id{ans.from_id}({user['nick']}), у вас уже имеется {privilege['name']} статус!"
        if user['status'] > int(id):
            return f"&#128219; @id{ans.from_id}({user['nick']}), вы не можете приобрести статус меньше вашего!"
        user['balance'] -= privilege['price']
        user['status'] = int(id)
        user['status_time'] = privilege['status_time']
        dumpjson(user, users)
        return f"&#127895; @id{ans.from_id}({user['nick']}), вы успешно приобрели: {privilege['name']} статус!\n&#128184; С вашего счета снято: {task(privilege['price'])}\n&#9732; Ваш текущий баланс: {task(user['balance'])} метеоров."
    if int(category) == 2:
        starship = find("id", int(id), starships)
        if not starship:
            return f"&#128219; @id{ans.from_id}({user['nick']}), такого товара не существует!"
        if user['balance'] < starship['price']:
            return f"&#128219; @id{ans.from_id}({user['nick']}), у вас не хватает метеоров!\n&#127895; Стоимость звездолета {starship['name']}: {task(starship['price'])} метеоров\n&#9732; Ваш текущий баланс: {task(user['balance'])} метеоров."
        if user['starship'] == starship['id']:
            return f"&#128219; @id{ans.from_id}({user['nick']}), у вас уже имеется звездолет {starship['name']}!"
        if user['starship'] > int(id):
            return f"&#128219; @id{ans.from_id}({user['nick']}), вы не можете приобрести звездолет меньшего класса, чем у вас имеется!"
        priv = find("id", user['status'], privileges)
        add_xp(user, priv, users)
        if user['xp'] >= 1000:
            try:
                await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
            except Exception:
                print(f"У пользователя {user['nick']} закрыт личные сообщения!")
        user['balance'] -= starship['price']
        user['starship'] = int(id)
        dumpjson(user, users)
        return f"&#127895; @id{ans.from_id}({user['nick']}), вы успешно приобрели: звездолет {starship['name']}!\n&#128184; С вашего счета снято: {task(starship['price'])}\n&#9732; Ваш текущий баланс: {task(user['balance'])} метеоров."
    return f"&#128219; @id{ans.from_id}({user['nick']}), такой категории в магазине не существует!"

# Продажа
@bp.on.message(text=["продать звездолет", "продай звездолет", "ghjlfq pdtpljktn", "ghjlfnm pdtpljktn"])
async def sell_starship(ans: Message):
    user = find("id", ans.from_id, users)
    starship = find("id", user['starship'], starships)
    if not starship:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас отсутствует звездолет!"
    priv = find("id", user['status'], privileges)
    add_xp(user, priv, users)
    if user['xp'] >= 1000:
        try:
            await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
        except Exception:
            print(f"У пользователя {user['nick']} закрыт личные сообщения!")
    user['starship'] = 0
    user['balance'] += int(starship['price']/100*50)
    dumpjson(user, users)
    return f"&#128176; @id{ans.from_id}({user['nick']}), вы успешно продали звездолет {starship['name']} за {task(int(starship['price']/100*50))}(50%) \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"