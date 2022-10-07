from vkbottle.bot import Blueprint, Message
from helper import *

bp = Blueprint("Стандарт")
bp.labeler.vbml_ignore_case = True
users = "Other/users.json"
privileges = "Other/privilege.json"
jobs = "Other/jobs.json"

#bp.on.message(text=["работы"])
async def job_list(ans: Message): 
    ...