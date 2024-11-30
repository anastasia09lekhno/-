import re

def evaluate_expression(expression, context):
    """
    Вычисляет константные выражения на основе текущего контекста.
    """
    # Убираем символы `|`
    expression = expression.strip("|")
    
    # Заменяем имена переменных их значениями из контекста
    for key, value in context.items():
        expression = expression.replace(key, str(value))
    
    # Используем eval для вычисления выражения
    try:
        result = eval(expression)
        return result
    except Exception as e:
        raise ValueError(f"Ошибка вычисления выражения '{expression}': {e}")


def convert_to_custom_language(data, context=None):
    """
    Конвертирует TOML-данные в целевой конфигурационный язык.
    """
    if context is None:
        context = {}  # Контекст для вычислений

    if isinstance(data, dict):
        output = "'("
        for key, value in data.items():
            converted_key = f"[[{key}]]"
            converted_value = convert_to_custom_language(value, context)
            output += f"{converted_key} {converted_value} "
        output += ")"
        return output

    elif isinstance(data, list):
        output = "'("
        for item in data:
            converted_item = convert_to_custom_language(item, context)
            output += f"{converted_item} "
        output += ")"
        return output

    elif isinstance(data, str):
        # Проверяем, является ли строка выражением для вычисления
        if re.match(r"^\|.*\|$", data):
            result = evaluate_expression(data, context)
            return str(result)
        else:
            return f"[[{data}]]"

    elif isinstance(data, (int, float)):
        return str(data)

    else:
        raise ValueError(f"Неподдерживаемый тип данных: {type(data)}")
