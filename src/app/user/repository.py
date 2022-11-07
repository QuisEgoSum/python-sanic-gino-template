from src.app.user.model import UserModel


async def save(user: dict) -> UserModel:
    return await UserModel(**user).create()

