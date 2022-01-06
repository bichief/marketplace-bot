from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.db_api import schemas
from utils.db_api.schemas.user import User


class CRUDUser:
    def init(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        Parameters
        * model: A SQLAlchemy model class
        * schema: A Pydantic model (schema) class
        """

    async def get(self, session: Session, id: int) -> User:
        result = await session.execute(select(User).order_by(User.id).filter(User.id == id))
        return result.scalars().first()

    async def get_all(self, session: Session) -> List[schemas.UserCreate]:
        result = await session.execute(select(User))
        return result.scalars().all()

    async def create_user(self, session: Session):
        db_user = User()
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return user.from_orm(db_user)

    async def delete_user(self, session: Session, id: int):
        row = await session.execute(select(User).where(User.id == id))
        row = row.scalar_one()
        await session.delete(row)
        await session.commit()
        return {'user': 'delete'}
