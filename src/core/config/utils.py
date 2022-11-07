import re


def unify_name(name: str):
    """
    Преобразует имена к виду, необходимому для формирования имени переменной окружения:
    1. Заменяет все не цифровые и не англоязычные символы на _
    2. Приводит к верхнему регистру
    """
    return re.sub(pattern='[^a-zA-Z0-9]', repl='_', flags=re.DOTALL, string=name.upper())
