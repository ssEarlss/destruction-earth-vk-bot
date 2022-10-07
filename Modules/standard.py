from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from helper import *
import heapq

bp = Blueprint("Стандарт")
bp.labeler.vbml_ignore_case = True
users = "Other/users.json"
privileges = "Other/privilege.json"
clans = "Other/clans.json"
right = "Other/rights.json"
starships = 'Other/starship.json'
locations = 'Other/locations.json'

# Начало
@bp.on.message(text="start")
async def test(ans: Message):
    keyboard = (
    Keyboard(inline=False)
    .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("&#128722; Магазин", {"standard": "shop"}))
    .add(Text("&#127941; Топ", {"standard": "top"}))
    .row()
    .add(Text("&#128737; Клан", {"standard": "clan"}))
    .add(Text("&#128301; Локации", {"standard": "locations"}))
    .row()
    .add(Text("&#128377; Игры", {"standard": "game"}))
    .add(Text("&#128182; Заработок", {"standard": "earning"}))
    .row()
    .add(Text("&#128295; Настройки", {"standard": "settings"}))
    .add(Text("&#128220; Помощь", {"standard": "help"}))
    )
    await ans.answer("Если ты новенький, то нажимай на кнопку 'Помощь'.", keyboard=keyboard)

@bp.on.message(text=["меню", "менб", "мен", "мен.", "мень"])
@bp.on.message(payload={"standard": "menu"})
async def menu(ans: Message):
    user = find("id", ans.from_id, users)
    user['buttons'] = True
    dumpjson(user, users)
    keyboard = (
    Keyboard(inline=False)
    .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("&#128722; Магазин", {"standard": "shop"}))
    .add(Text("&#127941; Топ", {"standard": "top"}))
    .row()
    .add(Text("&#128737; Клан", {"standard": "clan"}))
    .add(Text("&#128301; Локации", {"standard": "locations"}))
    .row()
    .add(Text("&#128377; Игры", {"standard": "game"}))
    .add(Text("&#128182; Заработок", {"standard": "earning"}))
    .row()
    .add(Text("&#128295; Настройки", {"standard": "settings"}))
    .add(Text("&#128220; Помощь", {"standard": "help"}))
    )
    await ans.answer(f"&#128218; @id{user['id']}({user['nick']}), главное меню:", keyboard=keyboard)

@bp.on.message(payload={"standard": "game"})
async def game(ans: Message):
    user = find("id", ans.from_id, users)
    keyboard = (
    Keyboard(inline=False)
    .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("&#127920; Казино", {"standard": "casino"}))
    .add(Text("&#127922; Кости", {"standard": "dice"}))
    .row()
    .add(Text("&#128220; Помощь", {"standard": "help"}))
    .row()
    .add(Text("&#9664;&#65039; Меню", {"standard": "menu"}))
    )
    await ans.answer(f"&#128377; @id{user['id']}({user['nick']}), игры:", keyboard=keyboard)

@bp.on.message(payload={"standard": "settings"})
async def settings(ans: Message):
    user = find("id", ans.from_id, users)
    keyboard = (
    Keyboard(inline=False)
    .add(Text("&#127899; Включить кнопки", {"standard": "on_buttons"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("&#127899; Выключить кнопки", {"standard": "off_buttons"}), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("&#128220; Помощь", {"standard": "help"}))
    .row()
    .add(Text("&#9664;&#65039; Меню", {"standard": "menu"}))
    )
    await ans.answer(f"&#128295; @id{user['id']}({user['nick']}), настройки:", keyboard=keyboard)
@bp.on.message(text=["включить кнопки", "вкл кнопки", "drk.xbnm ryjgrb", "drk ryjgrb"])
@bp.on.message(payload={"standard": "on_buttons"})
async def on_buttons(ans: Message):
    user = find("id", ans.from_id, users)
    user['buttons'] = True
    dumpjson(user, users)
    keyboard = (
    Keyboard(inline=False)
    .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("&#128722; Магазин", {"standard": "shop"}))
    .add(Text("&#127941; Топ", {"standard": "top"}))
    .row()
    .add(Text("&#128737; Клан", {"standard": "clan"}))
    .add(Text("&#128301; Локации", {"standard": "locations"}))
    .row()
    .add(Text("&#128377; Игры", {"standard": "game"}))
    .add(Text("&#128182; Заработок", {"standard": "earning"}))
    .row()
    .add(Text("&#128220; Помощь", {"standard": "help"}))
    )
    await ans.answer(f"&#127899; @id{user['id']}({user['nick']}), вы включили кнопки!", keyboard=keyboard)
@bp.on.message(text=["выключить кнопки", "выкл кнопки", "dsrk.xbnm ryjgrb", "dsrk ryjgrb"])
@bp.on.message(payload={"standard": "off_buttons"})
async def off_buttons(ans: Message):
    user = find("id", ans.from_id, users)
    user['buttons'] = False
    dumpjson(user, users)
    keyboard = (Keyboard(inline=False))
    await ans.answer(f"&#127899; @id{user['id']}({user['nick']}), вы выключили кнопки!", keyboard=keyboard)

# Информации
@bp.on.message(text=["профиль", "profile", "проф", "ghja", "ghjabkm"])
@bp.on.message(payload={"standard": "profile"})
async def profile(ans: Message):
    user = find("id", ans.from_id, users)
    statuss = find("id", user['status'], privileges)
    rightss = find("rights", user['rights'], right)
    location = find("id", user['location'], locations)
    clanss, starship, status_time, rights, keyboard, status, emojis = "Отсутствует", "Отсутствует", "", "", "", "Пользователь", "&#127895;"
    if statuss:
        status = f"{statuss['name']}"
        status_time = f"\n&#8986; Статус действует еще: {user['status_time']} д."
        emojis = statuss['emoji']
    if user['rights'] != 0:
        rights = f"\n&#9878; Права: {rightss['name']}"
    if user["clan"] is not None:
        clan = find("uid", user['clan'], clans)
        clanss = f"{clan['name']}"
    if user['starship'] != 0:
        starshipss = find('id', user['starship'], starships)
        starship = f"{starshipss['name']}"
    if user['buttons'] == True:
        keyboard = (
        Keyboard(inline=False)
        .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("&#128722; Магазин", {"standard": "shop"}))
        .add(Text("&#127941; Топ", {"standard": "top"}))
        .row()
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
    await ans.answer(f"&#128187; @id{ans.from_id}({user['nick']}), ваш профиль:\n&#9881; ID: {user['uid']}\n&#128172; Ник: {user['nick']}\n&#127915; Уровень: {task(user['lvl'])}\n&#9203; Опыт: {user['xp']}/1.000 {rights}\n{emojis} Статус: {status}{status_time}\n&#128737; Клан: {clanss}\n&#128640; Звездолет: {starship}\n&#128301; Местоположение: {location['name']}\n&#9732; Метеоры: {task(user['balance'])}\n&#128179; Банк метеоров: {task(user['bank'])}\n&#127878; Уничтожено планет: {task(user['destroyed_planets'])}", keyboard=keyboard)

@bp.on.message(text="чек <id>")
async def check_profile(ans: Message, id):
    userss = find("id", ans.from_id, users)
    user = find("uid", int(id), users)
    if not user:
        return f"&#128219; @id{ans.from_id}({userss['nick']}), такого человека не существует!"
    statuss = find("id", user['status'], privileges)
    rightss = find("rights", user['rights'], right)
    location = find("id", user['location'], locations)
    rights, status_time, clanss, starship, status, emojis = "", "", "Отсутствует", "Отсутствует", "Пользователь", "&#127895;"
    if statuss is not None and statuss['id'] > 0:
        status_time = f"\n&#8986; Статус действует еще: {user['status_time']} д."
        status = f"{statuss['name']}"
        emojis = statuss['emoji']
    if user['rights'] != 0:
        rights = f"\n&#9878; Права: {rightss['name']}"
    if user["clan"] is not None:
        clan = find("uid", user['clan'], clans)
        clanss = f"{clan['name']}"
    if user['starship'] != 0:
        starshipss = find('id', user['starship'], starships)
        starship = f"{starshipss['name']}"
    return f"&#128187; @id{ans.from_id}({userss['nick']}), профиль пользователя @id{user['id']}({user['nick']}):\n&#9881; ID: {user['uid']}\n&#128172; Ник: {user['nick']}\n&#127915; Уровень: {task(user['lvl'])}\n&#9203; Опыт: {user['xp']}/1.000 {rights}\n{emojis} Статус: {status}{status_time}\n&#128737; Клан: {clanss}\n&#128640; Звездолет: {starship}\n&#128301; Местоположение: {location['name']}\n&#9732; Метеоры: {task(user['balance'])}\n&#128179; Банк метеоров: {task(user['bank'])}\n&#127878; Уничтожено планет: {task(user['destroyed_planets'])}"

@bp.on.message(text=["топ", "топы", "top", "tops", "njg"])
@bp.on.message(payload={"standard": "top"})
async def tops(ans: Message):
    user = find("id", ans.from_id, users)
    topmoney = f"&#127941; @id{ans.from_id}({user['nick']}), топ богатых:\n"
    topclans = f"\n ====================== \n \n &#128737; Топ кланов:\n"
    num, nums, money_top, clan_top = 49, 49, [], []
    for i in loadjson(users):
        money_top.append((i['balance'] + i['bank'], i['id'], i['nick'], i['uid']))
    for i in heapq.nlargest(5, money_top):
        topmoney += f"&#{num};&#8419; @id{i[1]}({i[2]}) \n⠀&#9881; ID: {i[3]} \n⠀&#128179; Баланс: {task(i[0])} метеоров\n\n"
        num += 1
    for i in loadjson(clans):
        clan_top.append((i['balance'], i['name'], i['users'], i['owner'], i['lvl']))
    for i in heapq.nlargest(5, clan_top):
        topclans += f"&#{nums};&#8419; @id{i[3]}({i[1]}) \n⠀&#127991; Уровень: {i[4]} \n⠀&#128483; Людей: {i[2]}/100 \n⠀&#128179; Баланс: {task(i[0])} метеоров\n"
        nums += 1
    await ans.answer(topmoney + topclans)


@bp.on.message(text=["ник <name>", "ybr <name>"])
async def name(ans: Message, name):
    user = find("id", ans.from_id, users)
    if user['status'] < 2:
        return f"&#128219; @id{ans.from_id}({user['nick']}), сменить ник можно лишь при наличии Титан статуса!"
    if user['balance'] < 500000:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров! \n &#128179; Стоимость смена ника: 500.000 метеоров \n &#9732; Сейчас у вас на счету: {task(user['balance'])} метеоров"
    if len(name) > 15:
        return f"&#128219; @id{ans.from_id}({user['nick']}), название ника слишком длинное! \n &#128199; Максимальная длина: 15 символов!"
    if name == user['nick']:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас уже такой ник!"
    for i in loadjson(users):
        if str.lower(i['nick']) == str.lower(name):
            return f"&#128219; @id{ans.from_id}({user['nick']}), такой ник уже существует, выберите другой!"
    names = user['nick']
    user['balance'] -= 500000
    user['nick'] = name
    dumpjson(user, users)
    return f" @id{ans.from_id}({names}), вы успешно сменили ник на @id{ans.from_id}({user['nick']}) \n &#128184; С вашего счета снято: 500.000 метеоров \n &#9732; Сейчас у вас на счету: {task(user['balance'])} метеоров"

# Банковские махинации
@bp.on.message(text=["банк пополнить <some>", "пополнить банк <some>"])
async def add_bank(ans: Message, some):
    user = find("id", ans.from_id, users)
    if user['balance'] >= int(some) >= 1:
        user['balance'] -= int(some)
        user['bank'] += int(some)
        dumpjson(user, users)
        return f"&#128179; @id{ans.from_id}({user['nick']}), вы пополнили банк на {some} метеоров!"
    return f"&#128219 @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров! \n &#9732; Сейчас у вас на счету: {task(user['balance'])} метеоров"   
    
@bp.on.message(text=["банк снять <some>", "снять банк <some>"])
async def take_bank(ans: Message, some):
    user = find("id", ans.from_id, users)
    if user['bank'] >= int(some) >= 1:
        user['balance'] += int(some)
        user['bank'] -= int(some)
        dumpjson(user, users)
        return f"&#128179; @id{ans.from_id}({user['nick']}), вы сняли с банка {some} метеоров!"
    return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров! \n &#9732; Сейчас у вас на счету: {task(user['balance'])} метеоров"


@bp.on.message(text=["звездолет", "транспорт", "тс"])
async def starship(ans: Message):
    user = find("id", ans.from_id, users)
    if user['starship'] == 0:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас отсутствует звездолет!"
    starship = find("id", user['starship'], starships)
    return f"&#128640; @id{ans.from_id}({user['nick']}), ваш звездолет: \n&#127991; Название: {starship['name']} \n&#9889;&#65039; Дальность: {task(starship['range'])} А.Е. \n&#9876; Урон: {task(starship['damage'])}"

@bp.on.message(text=["локации", "локация", "лока", "локи"])
@bp.on.message(payload={"standard": "locations"})
async def location(ans: Message):
    user = find("id", ans.from_id, users)
    location = find("id", user['location'], locations)
    loc, num = "", 49
    for i in loadjson(locations):
        loc += f"\n&#{num};&#8419; {i['emoji']} {i['name']} \n⠀&#9881; Номер: {i['id']} \n⠀&#128207; Расстояние: {task(i['distance'])} А.Е.\n⠀&#128179; Стоимость полета: {task(i['cost'])}\n"
        num += 1
    await ans.answer(f"&#128301; @id{ans.from_id}({user['nick']}), вы находитесь в локации '{location['name']}' \n\n&#128301; Локации:" + loc + "\n&#128220; Чтобы перелететь на другую локацию, напишите: перелет 'номер'.")

@bp.on.message(text=["перелет <id>", "перелететь <id>", "gthtktnb <id>", "gthtktntnm <id>"])
async def go_loc(ans: Message, id):
    user = find("id", ans.from_id, users)
    location = find("id", int(id), locations)
    starshipss = find("id", user['starship'], starships)
    if user['starship'] == 0:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас отсутствует звездолет!"
    if not location:
        return f"&#128219; @id{ans.from_id}({user['nick']}), такой локации не существует!"
    if user['location'] == location['id']:
        return f"&#128219; @id{ans.from_id}({user['nick']}), вы уже находитесь в данной локации!"
    if user['balance'] < location['cost']:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров! \n Стоимость перелета: {task(location['cost'])} метеоров. \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров."
    if starshipss['range'] < location['distance']:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вашего звездолета не хватает мощности! \n &#9889;&#65039; Дальность вашего звездолета: {task(starshipss['range'])} А.Е. \n &#128207; {location['name']}, расстояние: {task(location['distance'])} А.Е."
    user['balance'] -= location['cost']
    user['location'] = location['id']
    dumpjson(user, users)
    return f"@id{ans.from_id}({user['nick']}), вы перелетели в {location['name']} \n &#128184; С вашего счёта снято: {task(location['cost'])} метеоров. \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров."


@bp.on.message(text=["жалоба <texts>", "жб <texts>", "помогите <texts>", "тикет <texts>", ";fkj,f <texts>", ";, <texts>"])
async def ticket(ans: Message, texts):
    user = find("id", ans.from_id, users)
    if len(texts) > 150:
        return f"&#128219; @id{ans.from_id}({user['nick']}), жалоба слишком длинная!\n &#128199; Максимальная длина: 150 символов."
    await bp.api.messages.send(chat_id=2, message=f"&#128278; Пользователь @id{user['id']}({user['nick']})[ID: {user['uid']}] написал жалобу:\n&#128195; {texts}", random_id=0)
    return f"&#128278; @id{user['id']}({user['nick']}), ваша жалоба была отправлена! Ожидайте ответа в личных сообщениях бота!"


@bp.on.message(text=["help", "хелп", "помощь", "помоги", "[tkg", "зелп"])
@bp.on.message(payload={"standard": "help"})
async def help(ans: Message):
    user = find("id", ans.from_id, users)
    keyboard = ""
    if user['buttons'] == True:
        keyboard = (
        Keyboard(inline=False)
        .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("&#128722; Магазин", {"standard": "shop"}))
        .add(Text("&#127941; Топ", {"standard": "top"}))
        .row()
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
    await ans.answer(f"&#128220; @id{ans.from_id}({user['nick']}), вот какие команды я знаю:\n\n&#128214; Информация:\n⠀&#49;&#8419; &#128187; Профиль - посмотреть свой профиль.\n⠀&#50;&#8419; &#128209; Чек 'ID' - посмотреть профиль другого человека.\n⠀&#51;&#8419; &#127941; Топ - посмотреть топ богачей и кланов.\n\n&#128179; Банк:\n⠀&#49;&#8419; &#128179; Банк пополнить 'сумма' - пополнить банк.\n⠀&#50;&#8419; &#128179; Банк снять 'сумма' - снять с банка.\n\n&#128220; Магазин:\n⠀&#49;&#8419; &#128220; Магазин 'номер страницы' - посмотреть список товаров.\n⠀&#50;&#8419; &#128722; Купить 'ID' - купить товар.\n\n&#128176; Продажа:\n⠀&#49;&#8419; Продать звездолет - продать звездолет.\n⠀⠀&#9888; Вы получите только 50% от цены звездолета.\n\n&#128737; Клан:\n⠀&#49;&#8419; &#128737; Клан - информация о клане.\n⠀&#50;&#8419; &#128221; Создать клан 'название' - создать клан. \n⠀⠀&#128179; Стоимость: 100.000.000 метеоров.\n⠀&#51;&#8419; &#128466; Участники клана - показывает всех участников клана.\n⠀&#52;&#8419; &#128737; Чек клан 'название' - информация о клане.\n⠀&#53;&#8419; &#127895; Пополнить баланс клана 'сумма' - пополнение баланса клана.\n⠀&#54;&#8419; &#127895; Снять баланс клана 'сумма' - снятие баланса клана.\n⠀⠀&#9888; Снимать может только владелец клана.\n⠀&#55;&#8419; &#128236; Пригласить в клан 'nick' - пригласить в клан.\n⠀&#56;&#8419; &#128499; выгнать из клана 'nick' - выгнать из клан.\n\n&#128184; Заработок метеоров:\n⠀&#49;&#8419; &#10024; Разрушить метеор - заработать 10 метеоров.\n\n&#128377; Игры:\n⠀&#49;&#8419; &#127920; Казино 'сумма' - сыграть в казино.\n⠀⠀&#9888; Минимальная ставка: 500.\n⠀&#50;&#8419; &#127922; Кости 'сумма' - сыграть в кости\n⠀⠀&#9888; Минимальная ставка: 500.\n\n&#128301; Локации:\n⠀&#49;&#8419; &#128301; Локации - все лоакции.\n ⠀&#50;&#8419; &#128640; Перелет 'номер' - перелететь на локацию.\n⠀⠀&#128179; Стоимость перелета: 1.000.000.000 метеоров. \n\n&#128209; Прочее:\n⠀&#49;&#8419; &#128221; Ник 'name' - сменить ник.\n⠀⠀&#128179; Стоимость смена ника: 500.000 метеоров.\n⠀&#50;&#8419; &#127899; Включить/выключить кнопки - настройка кнопок.\n⠀&#51;&#8419; &#128278; Жалоба 'текст' - написать жалобу/предложение", keyboard=keyboard)

@bp.on.message(text="ahelp")
async def ahelp(ans: Message):
    user = find("id", ans.from_id, users)
    if user['rights'] <= 0:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав, чтобы использовать эту команду!"
    return f"&#128220; @id{ans.from_id}({user['nick']}), вот какие команды для администраторов я знаю:\n\n&#9732; Действия с метеорами:\n⠀&#49;&#8419; &#128184; выдать метеоры 'id' 'some' - выдача метеоров.\n⠀⠀&#9878; Уровень доступа: 3 'Разработчик'.\n⠀&#50;&#8419; &#128184; забрать метеоры 'id' 'some' - забрать метеоры.\n⠀⠀&#9878; Уровень доступа: 3 'Разработчик'.\n\n&#128737; Действия с кланами:\n⠀&#49;&#8419; &#10002;&#65039; Удалить клан 'id' - удаление клана.\n⠀⠀&#9878; Уровень доступа: 2 'Администратор'.\n\n&#128736; Действия с json files:\n⠀&#49;&#8419; &#128223; Изменить  json/'название'.json 'uid/id' 'id' 'one' 'two(int)'\n⠀⠀&#9878; Уровень доступа: 3 'Разработчик'."

@bp.on.private_message()
async def no_commands(ans: Message):
    user = find("id", ans.from_id, users)
    return f"&#10067; @id{ans.from_id}({user['nick']}), я не знаю такой команды. \n &#128220; Воспользуйтесь командой 'помощь', чтобы узнать все мои команды"