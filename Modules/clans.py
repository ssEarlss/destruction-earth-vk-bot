from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message
from helper import *
import heapq

bp = Blueprint("Стандарт")
bp.labeler.vbml_ignore_case = True
users = "Other/users.json"
clans = "Other/clans.json"
privileges = "Other/privilege.json"

@bp.on.message(text=["создать клан <name>", "create clan <name>"])
async def create_clan(ans: Message, name):
    user = find("id", ans.from_id, users)
    clan = find("name", name, clans)
    uid = maxuId(clans)
    lens = len(name)
    if user['balance'] < 100000000:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно метеоров! \n &#128179; Стоимость создания клана: 100.000.000 метеоров \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    if user['clan'] != None:
        return f"&#128219; @id{ans.from_id}({user['nick']}), вы не можете создать клан, так как вы находитесь в клане!"
    if lens > 15:
        return f"&#128219; @id{ans.from_id}({user['nick']}), название клана слишком длинное! \n &#128199; Максимальная длина: 15 символов!"
    for i in loadjson(clans):
        if str.lower(i['name']) == str.lower(name):
            return f"&#128219; @id{ans.from_id}({user['nick']}), клан с таким названием уже существует!"
    if not clan:
        push(clans, {
            "uid": uid,
            "name": name,
            "lvl": 0,
            "balance": 0,
            "owner": int(user['id']),
            "supervisor": None,
            "users": 1
        })
        priv = find("id", user['status'], privileges)
        add_xp(user, priv, users)
        if user['xp'] >= 1000:
            try:
                await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
            except Exception:
                print(f"У пользователя {user['nick']} закрыт личные сообщения!")
        user['balance'] -= 100000000
        user['clan'] = uid
        dumpjson(user, users)
        return f"&#128737; @id{ans.from_id}({user['nick']}), вы успешно создали клан с названием '{name}' \n &#128184; С вашего счёта списано: 100.000.000 метеоров \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    return f"&#128219; @id{ans.from_id}({user['nick']}), уже существует клан с названием '{name}'!"

@bp.on.message(text=["удалить клан", "delete clan"])
async def delete_clan(ans: Message):
    user = find("id", ans.from_id, users)
    if user['clan'] is None:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас отсутствует клан!"
    clan = find("uid", user['clan'], clans)
    if clan['owner'] != user['id']:
        return f"&#128219; Вы не можете удалить клан, так как вы не владелец клана {clan['name']}!"
    accept_delete = f"&#128205; Вы точно хотите удалить клан {clan['name']}?"
    #подтверждение удаление клана
    #return f"&#128737; @id{ans.from_id}({user['nick']}), вы успешно удалили клан {clan['name']}"

@bp.on.message(text=["клан", "rkfy", "clan"])
@bp.on.message(payload={"standard": "clan"})
async def info_clan(ans: Message):
    user = find("id", ans.from_id, users)
    keyboard, supervisors = "", "Отсутствует"
    if user['clan'] is None:
        return f"&#128737; @id{ans.from_id}({user['nick']}), у вас отсутствует клан.\n&#128220; Чтобы создать клан, напишите: создать клан 'название'\n&#128179; Стоимость создания клана: 100.000.000 метеоров\n&#9732; Ваш текущий баланс: {task(user['balance'])} метеоров\n\n&#128220; Чтобы попасть в клан, необязательно его создавать, нужно лишь ждать приглашения в клан от другого человека!"
    clan = find("uid", user['clan'], clans)
    owner = find("id", clan['owner'], users)
    if clan['supervisor'] is not None:
        supervisor = find("id", clan['supervisor'], users)
        supervisors = f"@id{clan['supervisor']}({supervisor['nick']})"
    if user['buttons'] is True:
        keyboard = (
            Keyboard(inline=False)
            .add(Text("&#128187; Профиль", {"standard": "profile"}), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text("&#128466; Участники клана", {"standard": "people_clan"}))
            .row()
            .add(Text("&#128220; Помощь", {"standard": "help"}))
            .row()
            .add(Text("&#9664;&#65039; Меню", {"standard": "menu"}))
            )
    await ans.answer(f"&#128737; @id{ans.from_id}({user['nick']}), вы состоите в клане:\n&#9881; ID: {clan['uid']}\n&#128278; Название: {clan['name']}\n&#127991; Уровень: {clan['lvl']}\n&#9732; Метеоров: {task(clan['balance'])}\n&#128305; Владелец: @id{clan['owner']}({owner['nick']})\n&#9884; Руководитель: {supervisors}\n&#128483; Людей: {clan['users']}/100", keyboard=keyboard)

@bp.on.message(text=["участники клана", "участники клан", "участник клана", "участник клан", "exfcnybrb rkfyf"])
@bp.on.message(payload={"standard": "people_clan"})
async def check_people_clan(ans: Message):
    user = find("id", ans.from_id, users)
    clan = find("uid", user['clan'], clans)
    if not clan:
        return f"&#128737; @id{ans.from_id}({user['nick']}), у вас отсутствует клан!"
    people, peoples = [], ""
    for i in loadjson(users):
        if i['clan'] == clan['uid']:
            people.append((i['balance'] + i['bank'], i['id'], i['nick']))
    for i in heapq.nlargest(3, people):
        peoples += f"&#128188; @id{i[1]}({i[2]}) - {task(i[0])} метеоров.\n"
    await ans.answer(f"&#128466; @id{ans.from_id}({user['nick']}), список участников клана '@id{clan['owner']}({clan['name']})':\n" + peoples)

@bp.on.message(text=["чек клан <name>", "клан чек <name>", "клан <name>"])
async def check_clan(ans: Message, name):
    user = find("id", ans.from_id, users)
    clan = find("name", name, clans)
    if not clan:
        return f"&#128737; @id{ans.from_id}({user['nick']}), такого клана не существует!"
    owner = find("id", clan['owner'], users)
    supervisors = "Отсутствует"
    if clan['supervisor'] is not None:
        supervisor = find("id", clan['supervisor'], users)
        supervisors = f"@id{clan['supervisor']}({supervisor['nick']})"
    return f"&#128737; @id{ans.from_id}({user['nick']}), информация о клане @id{owner['id']}({clan['name']}):\n&#9881; ID: {clan['uid']}\n&#128278; Название: {clan['name']}\n&#127991; Уровень: {clan['lvl']}\n&#9732; Метеоров: {task(clan['balance'])}\n&#128305; Владелец: @id{clan['owner']}({owner['nick']})\n&#9884; Руководитель: {supervisors}\n&#128483; Людей: {clan['users']}/100"

@bp.on.message(text=["пополнить баланс клана <some>", "пополнить баланс клан <some>", "пополнить клан <some>", "пополнить банк клан <some>", "пополнить банк клана <some>"])
async def add_money_clan(ans: Message, some):
    user = find("id", ans.from_id, users)
    clan = find("uid", user['clan'], clans)
    if user['clan'] is None:
        return f"&#128737; @id{ans.from_id}({user['nick']}), у вас отсутствует клан."
    if user['balance'] < int(some):
        return f"&#128737; @id{ans.from_id}({user['nick']}), вы указали метеоров больше, чем у вас есть! \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    user['balance'] -= int(some)
    clan['balance'] += int(some)
    dumpjson(user, users)
    print(dumpjson(clan, clans))
    return f"&#127895; @id{ans.from_id}({user['nick']}), вы пополнили баланс клана на {task(int(some))} метеоров! \n &#128179; Текущий баланс клана: {task(clan['balance'])} \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"

@bp.on.message(text=["снять баланс клана <some>", "снять баланс клан <some>", "снять клан <some>"])
async def take_money_clan(ans: Message, some):
    user = find("id", ans.from_id, users)
    clan = find("uid", user['clan'], clans)
    if user['clan'] is None:
        return f"&#128737; @id{ans.from_id}({user['nick']}), у вас отсутствует клан."
    if clan['owner'] != user['id']:
        return f"&#128737; @id{ans.from_id}({user['nick']}), снять с баланса клана может только владелец!"
    if clan['balance'] < int(some):
        return f"&#128737; @id{ans.from_id}({user['nick']}), вы указали метеоров больше, чем имеется на балансе клана! \n &#128179; Текущий баланс клана: {task(clan['balance'])} \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"
    user['balance'] += int(some)
    clan['balance'] -= int(some)
    dumpjson(clan, clans)
    dumpjson(user, users)
    return f"&#127895; @id{ans.from_id}({user['nick']}), вы сняли с баланса клана {task(int(some))} метеоров! \n &#128179; Текущий баланс клана: {task(clan['balance'])} \n &#9732; Ваш текущий баланс: {task(user['balance'])} метеоров"

@bp.on.message(text=["добавить в клан <nick>", "пригласить в клан <nick>"])
async def add_user_clan(ans: Message, nick):
    user = find("id", ans.from_id, users)
    if user['clan'] is None:
        return f"&#128737; @id{ans.from_id}({user['nick']}), у вас отсутствует клан."
    userss = find("nick", nick, users)
    if not userss:
        return f"&#128737; @id{ans.from_id}({user['nick']}), такого пользователя не существует!"
    clan = find("uid", user['clan'], clans)
    if clan['owner'] != user['id'] and clan['supervisor'] != user['id']:
        return f"&#128737; @id{ans.from_id}({user['nick']}), вы не можете приглашать людей в клан! \n Приглашать может только владелец и руководитель!"
    if userss['clan'] is not None:
        return f"&#128737; @id{ans.from_id}({user['nick']}), данный человек уже находится в клане!"
    priv = find("id", user['status'], privileges)
    add_xp(user, priv, users)
    if user['xp'] >= 1000:
        try:
            await ans.answer(f"&#128226; @id{user['id']}({user['nick']}), вы повысили свой уровень!")
        except Exception:
            print(f"У пользователя {user['nick']} закрыт личные сообщения!")
    userss['clan'] = user['clan']
    clan['users'] += 1
    dumpjson(userss, users)
    dumpjson(clan, clans)
    try:
        await bp.api.messages.send(peer_id=userss['id'], message=f"&#128226; @id{userss['id']}({userss['nick']}), вы были добавлены в клан @id{user['id']}({clan['name']})", random_id=0)
    except Exception:
        print(f"У пользователя {userss['nick']} закрыт личные сообщения!")
    return f"&#128233; @id{ans.from_id}({user['nick']}), вы успешно добавили пользователя @id{userss['id']}({userss['nick']}) в клан {clan['name']}"

@bp.on.message(text=["удалить из клана <nick>", "выгнать из клана <nick>", "кикнуть с клана <nick>", "выгнать с клана <nick>", "удалить с клана <nick>"])
async def del_user_clan(ans: Message, nick):
    user = find("id", ans.from_id, users)
    if user['clan'] is None:
        return f"&#128737; @id{ans.from_id}({user['nick']}), у вас отсутствует клан."
    clan = find("uid", user['clan'], clans)
    if clan['owner'] != user['id'] and clan['supervisor'] != user['id']:
        return f"&#128737; @id{ans.from_id}({user['nick']}), вы не можете изгонять людей из клан! \n Изгонять может только владелец и руководитель!"
    userss = find("nick", nick, users)
    if not userss:
        return f"&#128737; @id{ans.from_id}({user['nick']}), такого пользователя не существует!"
    if userss['clan'] != user['clan']:
        return f"&#128737; @id{ans.from_id}({user['nick']}), данный пользователь не состоит в вашем клане!"
    if userss['id'] == clan['owner']:
        return f"&#128737; @id{ans.from_id}({user['nick']}), вы не можете изгнать владельца из клана!"
    if userss['id'] == clan['supervisor']:
        clan['supervisor'] = None
    userss['clan'] = None
    clan['users'] -= 1
    dumpjson(userss, users)
    dumpjson(clan, clans)
    try:
        await bp.api.messages.send(peer_id=userss['id'], message=f"&#128226; @id{userss['id']}({userss['nick']}), вы были изгнаны человеком @id{user['id']}({user['nick']}) из клана @id{user['id']}({clan['name']})", random_id=0)
    except Exception:
        print(f"У пользователя {userss['nick']} закрыт личные сообщения!")
    return f" @id{ans.from_id}({user['nick']}), вы успешно изгнали пользователя @id{userss['id']}({userss['nick']}) из клана!"