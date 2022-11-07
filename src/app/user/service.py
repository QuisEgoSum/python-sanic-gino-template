from src.app.user.schemas import CreateUser


async def create(user: CreateUser):
    return user.dict()
