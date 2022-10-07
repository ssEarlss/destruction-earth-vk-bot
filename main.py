from vkbottle.bot import Bot, Message
from vkbottle import load_blueprints_from_package, BaseMiddleware
from helper import *

config = "Other/Settings/config.json"
users = "Other/users.json"

bot = Bot(loadjson(config)[0]["token"])

for bp in load_blueprints_from_package("Modules"):
    bp.load(bot)

class AllMessages(BaseMiddleware[Message]):
    async def pre(self):
        users_info = await bot.api.users.get(self.event.from_id)
        user = find("id", self.event.from_id, users)
        if not user:
            push(users, {
                "id": self.event.from_id,
                "uid": maxuId(users),
                "nick": users_info[0].first_name,
                "lvl": 0,
                "xp": 0,
                "rights": 0,
                "status": 0,
                "status_time": 0,
                "job": None,
                "balance": 0,
                "bank": 0,
                "starship": 0,
                "location": 1,
                "clan": None,
                "destroyed_planets": 0,
                "mute": False,
                "mute_time": 0,
                "warns": 0,
                "ban": False,
                "buttons": True
            })

bot.labeler.message_view.register_middleware(AllMessages)
bot.run_forever()