from sqlalchemy import select
from validator import UserValidator
from models import UserOrm, new_session
from random import randint


class UserRepository:
    @classmethod
    async def register(cls, user_validator: UserValidator) -> str:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().all()

            if not user_from_table:
                if user_data['password']:
                    new_user = UserOrm(**user_data)
                    session.add(new_user)
                    await session.commit()
                    return 'Пользователь зарегистрирован'
                else:
                    return 'Пароль не должен быть пустым'
            else:
                return 'Эта почта уже занята'

    @classmethod
    async def login(cls, user_validator: UserValidator) -> str:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().first()

            if user_from_table:
                if user_data['password'] and user_from_table.password == user_data['password']:
                    return 'Пользователь верифицирован'
                else:
                    return 'Неверный пароль'
            else:
                return 'Пользователь с такой почтой не найден'

    @classmethod
    async def edit(cls, user_validator: UserValidator) -> dict:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().first()

            status = {}

            if user_from_table:
                if user_data['wishes'] is not None:
                    user_from_table.wishes = user_data['wishes']
                    status['wishes'] = 'update'
                if user_data['calendar'] is not None:
                    user_from_table.calendar = user_data['calendar']
                    status['calendar'] = 'update'
                if user_data['test_result'] is not None:
                    user_from_table.test_result = user_data['test_result']
                    status['test_result'] = 'update'
                await session.commit()
            else:
                status['status'] = 'Пользователь с такой почтой не найден'

            return status

    @classmethod
    async def get_user_data(cls, user_validator: UserValidator) -> dict:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().first()

            if user_from_table:
                output = {
                    'wishes': user_from_table.wishes,
                    'calendar': user_from_table.calendar,
                    'test_result': user_from_table.test_result
                }
                return output
            else:
                return {'status': 'Пользователь с такой почтой не найден'}

    @classmethod
    async def reset_password_init(cls, user_validator: UserValidator) -> dict:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().first()

            if user_from_table:
                reset_code = randint(100000, 999999)

                user_from_table.last_reset_code = reset_code

                await session.commit()

                return {'email': user_from_table.email, 'reset_code': reset_code}
            else:
                return {'status': 'Пользователь с такой почтой не найден'}

    @classmethod
    async def reset_password_check(cls, user_validator: UserValidator) -> str:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().first()

            if user_from_table:
                if user_from_table.last_reset_code == user_data['last_reset_code']:
                    user_from_table.password = None
                    await session.commit()
                    return 'Пароль сброшен'
                else:
                    return 'Неверный код восстановления'
            else:
                return 'Пользователь с такой почтой не найден'

    @classmethod
    async def set_new_password(cls, user_validator: UserValidator) -> str:
        async with new_session() as session:
            user_data = user_validator.model_dump()

            query = select(UserOrm).where(UserOrm.email == user_data['email'])
            result = await session.execute(query)
            user_from_table = result.scalars().first()

            if user_from_table:
                if user_from_table.password is None:
                    if user_data['password']:
                        if user_data['password'] == user_data['re_password']:
                            user_from_table.password = user_data['password']
                            await session.commit()
                            return 'Пароль изменён'
                        else:
                            return 'Пароли не совпадают'
                    else:
                        return 'Пароль не должен быть пустым'
                else:
                    return 'Пароль не сброшен'
            else:
                return 'Пользователь с такой почтой не найден'

    @classmethod
    async def get_all_users(cls) -> str:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            users_from_table = result.scalars().all()

            for user in users_from_table:
                print(user.email, user.username)
            return 'Users unload'
