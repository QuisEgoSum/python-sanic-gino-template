import os
import typing
from dataclasses import dataclass

from src.core.config import Config
from src.core.config.project import project_name
from src.core.config.utils import unify_name
from src.utils.openapi import resolve_openapi_spec


@dataclass(frozen=True)
class EnvOption:
    # "Путь" к расположению значения внутри dict, например: ['server', 'http', 'port']
    parts: typing.List[str]
    # Openapi тип данных значения, например: 'integer', 'string', 'boolean'
    type: str
    # Сгенерированное имя переменной окружения, например: 'PROJECT_NAME_SERVER_HTTP_PORT'
    name: str


def _fill_env_list(schema: dict, result: typing.List[EnvOption], parts: typing.List[str]) -> None:
    """
    Рекурсивно заполняет массив result сгенерированными из схемы конфигурации элементами.
    """
    if 'allOf' in schema:
        for next_schema in schema['allOf']:
            _fill_env_list(next_schema, result, parts)
    elif schema['type'] == 'object' or 'object' in schema['type']:
        for name, next_schema in schema['properties'].items():
            current_parts = list(parts)
            current_parts.append(name)
            _fill_env_list(next_schema, result, current_parts)
    else:
        current_paths = list(parts)
        name_parts = [unify_name(env_name) for env_name in current_paths]
        # В начало будущего названия переменной окружения добавляем унифицированное название проекта
        name_parts.insert(0, project_name)
        result.append(EnvOption(current_paths, schema['type'], '_'.join(name_parts)))


def create_env_list_from_schema() -> typing.List[EnvOption]:
    """
    Генерирует массив env из схемы конфига
    """
    result: typing.List[EnvOption] = []
    _fill_env_list(resolve_openapi_spec(Config.schema_json()), result, [])
    return result


def assign_env_to_dict(config: dict) -> None:
    """
    Переопределяет в dict значения из переменных окружения в соответствии со сгенерированными
    именами переменных и расположением значения переменной в dict
    """
    env_list = create_env_list_from_schema()
    for env in env_list:
        value = os.environ.get(env.name, None)
        if value is None:
            continue
        current_config_dict = config
        last_part_index = len(env.parts) - 1
        for index, key in enumerate(env.parts):
            # Если это последний элемент назначаем значение по ключу
            if index == last_part_index:
                print(f'Applying a environment variable {env.name}')
                current_config_dict[key] = value
            # Иначе выбираем вложенный dict
            else:
                if key not in current_config_dict:
                    current_config_dict[key] = dict()
                current_config_dict = current_config_dict[key]



