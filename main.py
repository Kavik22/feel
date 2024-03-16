from fastapi import Depends, FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from repository import UserRepository
from validator import UserValidator, MailBodyValidator
from mailer import send_email
from models import engine, UserModelView, UserOrm, create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()

    await create_tables()
    print("База готова")
    yield
    # await delete_tables()
    # print("База очищена")


app = FastAPI(lifespan=lifespan)


@app.get("")
async def home():
    return "I'm alive"
    

@app.post("/register")
async def add_task(user: UserValidator = Depends()):
    status = await UserRepository.register(user)
    return {"status": status}


@app.post("/login")
async def home(user: UserValidator = Depends()):
    status = await UserRepository.login(user)
    return {"status": status}


@app.post("/edit")
async def edit(user: UserValidator = Depends()):
    status = await UserRepository.edit(user)
    return status


@app.post('/get_user_data')
async def get_user_data(user: UserValidator = Depends()):
    data = await UserRepository.get_user_data(user)
    return data


@app.post("/reset_password_init")
async def reset_password_init(tasks: BackgroundTasks, user: UserValidator = Depends()):
    status = await UserRepository.reset_password_init(user)
    if len(status) == 1:
        return status
    else:
        mail = {
            'to': [status['email']],
            'subject': 'Код для сброса пароля в приложении',
            'body': f'<h4>Ваш код для сброса пароля: {status["reset_code"]}</h4>',
        }

        tasks.add_task(send_email, mail)
        return {'status': 200, 'message': 'Письмо отправлено пользователю'}


@app.post("/reset_password_check")
async def reset_password_check(user: UserValidator = Depends()):
    status = await UserRepository.reset_password_check(user)
    return {'status': status}


@app.post("/set_new_password")
async def set_new_password(user: UserValidator = Depends()):
    status = await UserRepository.set_new_password(user)
    return {'status': status}


@app.get('/get_all_users')
async def get_all_users():
    status = await UserRepository.get_all_users()
    return {'status': status}


# @app.post("/send_email")
# async def scheduled_email(request: MailBodyValidator, tasks: BackgroundTasks):
#     data = request.dict()
#     tasks.add_task(send_email, data)
#     return {'status': 200, 'message': 'email has been scheduled'}


from starlette_admin.contrib.sqla import Admin

admin = Admin(engine, title="Feels good", base_url='/admin-42708426650')

admin.add_view(UserModelView(UserOrm))

admin.mount_to(app)
