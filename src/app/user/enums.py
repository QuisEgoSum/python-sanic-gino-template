import enum


class UserRoleEnum(str, enum.Enum):
    USER = 'USER',
    ADMIN = 'ADMIN',

