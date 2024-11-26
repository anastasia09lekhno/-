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
        port2 = "|port+1|"
        """
        # Ожидаемый результат
        expected_output = "'(server'(ip [[127.0.0.1]])'(port 8080)'(port2 8081))"

        # Парсим TOML
        parsed_data = parse_toml(toml_data)
        # Конвертируем в целевой формат
        output = convert_to_custom_language(parsed_data)

        # Сравнение результата с ожидаемым
        self.assertEqual(output, expected_output)

    def test_nested_structure(self):
        # Входные данные TOML
        toml_data = """
        [server]
        ip = "192.168.0.1"
        role = "backend"

        [server.details]
        cores = 4
        memory = 16
        """
        # Ожидаемый результат
        expected_output = "'(server'(ip [[192.168.0.1]])'(role [[backend]])'(details'(cores 4)'(memory 16)))"

        # Парсим TOML
        parsed_data = parse_toml(toml_data)
        # Конвертируем в целевой формат
        output = convert_to_custom_language(parsed_data)

        # Сравнение результата с ожидаемым
        self.assertEqual(output, expected_output)

    def test_constants_calculation(self):
        # Входные данные TOML
        toml_data = """
        [calculation]
        base = 100
        increment = 50
        total = "|base + increment|"
        """
        # Ожидаемый результат
        expected_output = "'(calculation'(base 100)'(increment 50)'(total 150))"

        # Парсим TOML
        parsed_data = parse_toml(toml_data)
        # Конвертируем в целевой формат
        output = convert_to_custom_language(parsed_data)

        # Сравнение результата с ожидаемым
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()

