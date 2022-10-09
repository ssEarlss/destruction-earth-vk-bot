from vkbottle.bot import Blueprint, Message
from vkbottle import DocMessagesUploader
from helper import *

bp = Blueprint("Стандарт")
bp.labeler.vbml_ignore_case = True
users = "Other/users.json"
privileges = "Other/privilege.json"
clans = "Other/clans.json"
right = "Other/rights.json"

@bp.on.message(text=["выдать метеоры <id> <some>", "добавить метеоры <id> <some>"])
async def give_money(ans: Message, id, some):
    user = find("id", ans.from_id, users)
    if user['rights'] < 3:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    userss = find("uid", int(id), users)
    if not userss:
        return f"&#128219; @id{ans.from_id}({user['nick']}), такого пользователя не существует!"
    userss['balance'] += int(some)
    dumpjson(userss, users)
    try:
        await bp.api.messages.send(peer_id=userss['id'], message=f"&#128226; @id{userss['id']}({userss['nick']}), администратор @id{user['id']}({user['nick']}) выдал вам {task(some)} метеоров.", random_id=0)
    except Exception:
        print(f"У пользователя {userss['nick']} закрыт личные сообщения!")
    return f"&#9832;&#65039; @id{ans.from_id}({user['nick']}), вы добавили пользователю @id{userss['id']}({(userss['nick'])}) {task(some)} метеоров. \n &#128179; У пользователя: {task(userss['balance'])} метеоров"

@bp.on.message(text="забрать метеоры <id> <some>")
async def take_money(ans: Message, id, some):
    user = find("id", ans.from_id, users)
    if user['rights'] < 3:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    userss = find("uid", int(id), users)
    if not userss:
        return f"&#128219; @id{ans.from_id}({user['nick']}), такого пользователя не существует!"
    userss['balance'] -= int(some)
    if userss['balance'] < 0:
        userss['balance'] = 0
    dumpjson(userss, users)
    try:
        await bp.api.messages.send(peer_id=userss['id'], message=f"&#128226; @id{userss['id']}({userss['nick']}), администратор @id{user['id']}({user['nick']}) забрал у вас {task(some)} метеоров.", random_id=0)
    except Exception:
        print(f"У пользователя {userss['nick']} закрыт личные сообщения!")
    return f"&#9832;&#65039; @id{ans.from_id}({user['nick']}), вы забрали у пользователя @id{userss['id']}({(userss['nick'])}) {task(some)} метеоров. \n &#128179; У пользователя: {task(userss['balance'])} метеоров"

@bp.on.message(text="удалить клан <id>")
async def delete_clan(ans: Message, id):
    user = find("id", ans.from_id, users)
    if user['rights'] < 2:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    clan = find("uid", int(id), clans)
    if not clan:
        return f"&#128219; @id{ans.from_id}({user['nick']}), такого клана не существует!"
    for i in loadjson(users):
        if i['clan'] == int(id):
            i['clan'] = None
            try:
                await bp.api.messages.send(peer_id=i['id'], message=f"&#128226; @id{i['id']}({i['nick']}), клан '{clan['name']}' был удален администратором @id{user['id']}({user['nick']})", random_id=0)
            except Exception:
                print(f"У пользователя {i['nick']} закрыт личные сообщения!")
            dumpjson(i, users)
    delete(clans, int(id))
    return f"&#128737; @id{ans.from_id}({user['nick']}), вы успешно удалили клан {clan['name']}[ID: {id}]!"

@bp.on.message(text="отправить <id> <texts>")
async def message_to_persone(ans: Message, id, texts):
    user = find("id", ans.from_id, users)
    if user['rights'] < 1:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    userss = find("uid", int(id), users)
    if not userss:
        return f"&#128219; @id{ans.from_id}({user['nick']}), такого пользователя не существует!"
    try:
        await bp.api.messages.send(peer_id=userss['id'], message=f"&#128213; @id{userss['id']}({userss['nick']}), сообщение от адмнистратора @id{user['id']}({user['nick']}):\n&#128195; {texts}", random_id=0)
        return f"&#128213; @id{user['id']}({user['nick']}), вы отправили пользователю @id{userss['id']}({userss['nick']}) сообщение:\n&#128195; {texts}"
    except Exception:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у пользователя @id{userss['id']}({userss['nick']}) закрыты личные сообщения!"

@bp.on.nessage(text="все пользователи")
async def all_users(ans:Message):
    user = find("id", ans.from_id, users)
    if user['rights'] < 2:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    num = 0
    for x in loadjson(users):
        num += 1
    return f" @id{ans.from_id}({user['nick']}), всего пользователей: {num}"

@bp.on.nessage(text="список пользователей")
async def all_users(ans:Message):
    user = find("id", ans.from_id, users)
    if user['rights'] < 2:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    text = ""
    for i in loadjson(users):
        text += f"@id{i['id']}({i['nick']})\n"
    await ans.answer(f"&#128424; @id{ans.from_id}({user['nick']}), список пользователей:\n" + text)

@bp.on.nessage(text="все кланы")
async def all_users(ans:Message):
    user = find("id", ans.from_id, users)
    if user['rights'] < 2:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    num = 0
    for x in loadjson(clans):
        num += 1
    return f" @id{ans.from_id}({user['nick']}), всего кланов: {num}"

@bp.on.nessage(text="список кланов")
async def all_users(ans:Message):
    user = find("id", ans.from_id, users)
    if user['rights'] < 2:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    text = ""
    for i in loadjson(clans):
        text += f"@id{i['owner']}({i['name']})\n"
    await ans.answer(f"&#128424; @id{ans.from_id}({user['nick']}), список кланов:\n" + text)


@bp.on.message(text="изменить <json> <ids> <id> <name> <num>")
async def dump_json(ans: Message, json, ids, id, name, num):
    user = find("id", ans.from_id, users)
    if user['rights'] < 3:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    jsons = find(ids, int(id), f"Other/{json}.json")
    if not jsons:
        return f"&#128219; @id{ans.from_id}({user['nick']}), такого {id} id в Other/{json}.json отсутсвует!"
    jsons[name] = int(num)
    dumpjson(jsons, f"Other/{json}.json")
    return f" @id{ans.from_id}({user['nick']}), вы изменили в Other/{json}.json файле пункты: \n {name} : {num}"

@bp.on.message(text="jsons")
async def log_users(ans: Message):
    user = find("id", ans.from_id, users)
    if user['rights'] < 3:
        return f"&#128219; @id{ans.from_id}({user['nick']}), у вас недостаточно прав это использовать!"
    userjss = DocMessagesUploader(bp.api)
    userjs = await userjss.upload("users.json", users, peer_id=ans.peer_id)
    clanjss = DocMessagesUploader(bp.api)
    clanjs = await clanjss.upload("clans.json", clans, peer_id=ans.peer_id)
    await bp.api.messages.send(chat_id=3, attachment=userjs, random_id=0)
    await bp.api.messages.send(chat_id=3, attachment=clanjs, random_id=0)
    return f"&#128251; @id{ans.from_id}({user['nick']}), users.json и clans.json отправлены в чат 'DE Jsons'"