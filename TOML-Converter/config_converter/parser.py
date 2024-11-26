import toml

def parse_toml(toml_data):
    """
    Функция для парсинга TOML в Python-словарь.
    """
    try:
        return toml.loads(toml_data)
    except toml.TomlDecodeError as e:
        raise ValueError(f"Ошибка парсинга TOML: {e}")
