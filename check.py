from typing import Any
from config import kanal_id
from aiogram.types import Message
from aiogram import Bot
from aiogram.filters import Filter


    
class CheksupChanel(Filter):
  async def __call__(self,message:Message,bot:Bot):
    for kanal in kanal_id:
        user_ststus=await bot.get_chat_member(kanal,message.from_user.id)
    if user_ststus.status in ['creator','administrator','member']:
        return False
    return True
