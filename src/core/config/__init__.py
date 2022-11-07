import os

import yaml
import argparse


from src.core.config.Сonfig import Config
from src.core.config.env import create_env_list_from_schema, assign_env_to_dict
from src.core.config.project import project_name, root_dir, project_metadata
from src.lib.alg import merge_dict_priority


DEFAULT_CONFIG_PATH = os.path.join(root_dir, 'config/default.yaml')


parser = argparse.ArgumentParser()
parser.add_argument(
    '--config',
    '-c',
    type=str,
    help='The path to the application configuration file'
)


def _get_override_config_path() -> str or None:
    """
    Возвращает заданный переменной окружения или параметром приложения путь к конфигурации
    Путь заданный переменной окружения является приоритетным
    """
    config_path = os.environ.get(
        f'{project_name}_CONFIG',
        parser.parse_args().config
    )
    # Относительный путь интерпретируем как путь относительно домашней директории проекта
    if config_path is not None and config_path.startswith('./'):
        config_path = os.path.abspath(os.path.join(root_dir, config_path))
    return config_path


def load_config() -> Config:
    """
    Создаёт объект конфига объединяя заданные параметры со следующим приоритетом:
    1. Переменные окружения
    2. Пользовательский конфиг
    3. Конфиг по умолчанию
    4. Значения по умолчанию заданные в классе конфигурации
    """
    with open(DEFAULT_CONFIG_PATH) as stream:
        config_dict = yaml.safe_load(stream) or dict()
    override_config_path = _get_override_config_path()
    if override_config_path is not None:
        print(f'Use override config {override_config_path}')
        with open(override_config_path) as stream:
            override_config_dict = yaml.safe_load(stream) or dict()
        config_dict = merge_dict_priority(config_dict, override_config_dict)
    assign_env_to_dict(config_dict)
    return Config(**config_dict)


config: Config = load_config()
