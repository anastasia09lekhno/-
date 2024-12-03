import unittest
from interpreter import Interpreter
import os
import yaml

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        """Создание временных файлов для тестов."""
        self.binary_file = "tests/temp_output.bin"
        self.memory_dump = "tests/temp_memory_dump.yaml"

    def tearDown(self):
        """Удаление временных файлов после тестов."""
        for file in [self.binary_file, self.memory_dump]:
            if os.path.exists(file):
                os.remove(file)

    def write_binary_file(self, filename, content):
        """Записывает бинарное содержимое в файл."""
        with open(filename, 'wb') as f:
            f.write(content)

    def test_load_and_bswap(self):
        # Пример программы с LOAD и BSWAP
        binary = bytes([0x52, 0xB0, 0xD0, 0x0A,  # LOAD 352, 346
                        0x16, 0x95, 0xE1, 0x05])  # BSWAP 810, 188
        self.write_binary_file(self.binary_file, binary)

        interpreter = Interpreter(self.binary_file, 0, 1024, self.memory_dump)
        interpreter.interpret()

        with open(self.memory_dump, "r") as f:
            memory = yaml.safe_load(f)

        self.assertEqual(memory[352], 346)
        self.assertEqual(memory[188], 0x056E)  # Реверс байтов значения

if __name__ == "__main__":
    unittest.main()
