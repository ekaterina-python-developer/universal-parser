import re


def collect_user_data(items: list[dict], key_name: str) -> list[str]:
    """Извлекает уникальные значения из результатов парсинга по ключу."""
    data_set = set()
    for item in items:
        for value in item.get(key_name, []):
            data_set.add(value)
    return list(data_set) if data_set else []


def filter_data(regex: str, text: str) -> list[str]:
    """Ищет совпадения и возвращает список уникальных строк."""
    found = set(re.findall(regex, text))
    return list(found) if found else []
