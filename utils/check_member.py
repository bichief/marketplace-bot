from data import config
from loader import bot


async def check_member(user_id):
    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
    if user_channel_status["status"] != 'left':
        return True
    else:
        return False