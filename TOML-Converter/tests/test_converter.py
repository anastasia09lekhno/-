import unittest
from config_converter.converter import convert_to_custom_language
from config_converter.parser import parse_toml


class TestConverter(unittest.TestCase):
    def test_simple_toml(self):
        # Входные данные TOML
        toml_data = """
        [server]
        ip = "127.0.0.1"
        port = 8080
        """
        # Ожидаемый результат
        expected_output = "( server (ip [[127.0.0.1]] port 8080 ) )"

        # Парсим TOML
        parsed_data = parse_toml(toml_data)
        # Конвертируем в целевой формат
        output = convert_to_custom_language(parsed_data)

        # Сравнение результата с ожидаемым
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
