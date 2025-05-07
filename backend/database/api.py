from fastapi import FastAPI
from database.settings import init_tortoise
from database.users.models import User
from database.companies.models import Company
from tortoise import Tortoise


app = FastAPI()

init_tortoise(app)


@app.post("/users")
async def create_user(email: str, password: str, company_name: str):
    user = await User.create(email=email, password=password, first_name="Олег", last_name="Подкудышный")
    company = await Company.create(name=company_name)
    user.set_password(password)
    user.company = company
    company.director = user
    await user.save()
    await company.save()

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "password": user.password,
        },
        "company": {
            "id": company.id,
            "name": company.name,
            "director": company.director.email
        }
    }


@app.get("/users")
async def get_users_list():
    users = await User.get(id=1)
    return {
        "id": users.id,
        "username": users.username,
        "password": users.password
    }


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int
):
    return await User.get(id=user_id).delete()


@app.delete("/")
async def delete_all():
    await Company.all().delete()
    await User.all().delete()

    return "ok"


@app.post("/")
async def added_users_in_company():
    company = await Company.get(id=3)
    for user in range(6, 10):
        new_user = await User.create(email=f"{user}@mail.ru", password=str(user), first_name=str(user), last_name=str(user+1))
        new_user.company = company
        await new_user.save()
    return "ok"
