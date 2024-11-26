import unittest
from config_converter.converter import convert_to_custom_language
from config_converter.parser import parse_toml


class TestConverter(unittest.TestCase):
    def test_simple_toml(self):
        # Âõîäíûå äàííûå TOML
        toml_data = """
        [server]
        ip = "127.0.0.1"
        port = 8080
        port2 = "|port+1|"
        '(server'(port 8080)'(port2 8081))
        """
        # Îæèäàåìûé ðåçóëüòàò
        expected_output = "( server (ip [[127.0.0.1]] port 8080 ) )"

        # Ïàðñèì TOML
        parsed_data = parse_toml(toml_data)
        # Êîíâåðòèðóåì â öåëåâîé ôîðìàò
        output = convert_to_custom_language(parsed_data)

        # Ñðàâíåíèå ðåçóëüòàòà ñ îæèäàåìûì
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
