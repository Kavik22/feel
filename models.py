from typing import Dict, Any
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

engine = create_async_engine("sqlite+aiosqlite:///feel.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    last_reset_code: Mapped[int | None]
    password: Mapped[str | None]
    re_password: Mapped[str | None]
    wishes: Mapped[str | None]
    calendar: Mapped[str | None]
    test_result: Mapped[str | None]


class UserModelView(ModelView):
    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        if str(request.url).split('/')[-2] != 'edit':
            async with new_session() as session:
                query = select(UserOrm)
                result = await session.execute(query)
                users_from_table = result.scalars().all()
                all_emails = [user.email for user in users_from_table]

            if data['email'] in all_emails:
                raise FormValidationError({'email': 'Эта почта уже занята'})
            return await super().validate(request, data)
