import unittest
from config_converter.converter import convert_to_custom_language
from config_converter.parser import parse_toml


class TestConverter(unittest.TestCase):
    def test_simple_toml(self):
        toml_data = """
        [server]
        ip = "127.0.0.1"
        port = 8080
        port2 = "|port+1|"
        """
        expected_output = "'( [[server]] '([[ip]] [[127.0.0.1]]) '([[port]] 8080) '([[port2]] 8081) )"

        parsed_data = parse_toml(toml_data)
        output = convert_to_custom_language(parsed_data)
        self.assertEqual(output, expected_output)

    def test_nested_structure(self):
        toml_data = """
        [server]
        ip = "192.168.0.1"
        role = "backend"

        [server.details]
        cores = 4
        memory = 16
        """
        expected_output = "'( [[server]] '([[ip]] [[192.168.0.1]]) '([[role]] [[backend]]) '([[details]] '([[cores]] 4) '([[memory]] 16) ) )"

        parsed_data = parse_toml(toml_data)
        output = convert_to_custom_language(parsed_data)
        self.assertEqual(output, expected_output)

    def test_constants_calculation(self):
        toml_data = """
        [ports]
        auth = 8080
        worker = "|auth + 1|"
        """
        expected_output = "'( [[ports]] '([[auth]] 8080) '([[worker]] 8081) )"

        parsed_data = parse_toml(toml_data)
        output = convert_to_custom_language(parsed_data)
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()

