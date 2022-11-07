from datetime import datetime

from gino import Gino

from src.core.config import config


db = Gino()


class DefaultModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)


class TimestampedModel(DefaultModel):
    created_at = db.Column(db.Integer(), nullable=False, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer(), nullable=False, default=lambda: int(datetime.now().timestamp()))


async def connect():
    await db.set_bind(config.database.uri)
