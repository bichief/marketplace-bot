from sqlalchemy.future import select
from sqlalchemy.orm import Session

from utils.db_api.schemas.user import User


class UserAdd:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_user(self, telegram_id: int, username: str):
        new_user = User(telegram_id=telegram_id, username=username)
        self.db_session.add(new_user)
        await self.db_session.flush()
