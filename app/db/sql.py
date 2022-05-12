import uuid

from sqlalchemy import Column, String, create_engine, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, declarative_base

from app.config import get_db_url

from .adapter import DataBaseAdapter, ModelUser

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column('first_name', String(50), nullable=False)
    second_name = Column('second_name', String(50), nullable=False)

    def __repr__(self):
        return f'User(id={self.id!r}, first_name={self.first_name!r}, second_name={self.second_name!r})'


class SQLAlchemyAdapter(DataBaseAdapter):

    engine = None

    def __init__(self):
        self.engine = create_engine(get_db_url(), echo=True, future=True)

    def get_user(self, uid: UUID) -> ModelUser:
        with Session(bind=self.engine) as session:
            user = session.scalars(select(User).where(User.id == uid)).one()
            return ModelUser(
                id=user.id,
                first_name=user.first_name,
                second_name=user.second_name
            )

    def create_user(self, user: ModelUser) -> UUID:
        with Session(bind=self.engine) as session:
            orm_user = User(
                id=uuid.uuid4(),
                first_name=user.first_name,
                second_name=user.second_name
            )
            session.add(orm_user)
            session.commit()

            return orm_user.id

    def delete_user(self, uid: UUID) -> None:
        with Session(bind=self.engine) as session:
            session.query(User).filter(User.id == uid).delete()
            session.commit()
