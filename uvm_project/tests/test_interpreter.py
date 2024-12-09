import unittest
from interpreter import Interpreter
import os

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.binary_file = "tests/bswap_vector.bin"
        self.memory_file = "tests/memory_dump.yaml"

    def tearDown(self):
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)

    def test_bswap_vector(self):
        # Ассемблируем программу
        assembler = Assembler("tests/bswap_vector.asm", self.binary_file, None)
        assembler.assemble()

        # Интерпретируем программу
        interpreter = Interpreter(self.binary_file, 0, 5, self.memory_file)
        interpreter.interpret()

        # Ожидаемые результаты
        expected_memory = {
            0: 0x78563412,  # Первый элемент после bswap
            1: 0x21436587,  # Второй элемент после bswap
            2: 0xEFBEADDE,  # Третий элемент после bswap
            3: 0xBEBAFECA,  # Четвертый элемент после bswap
            4: 0x0DF00BAD   # Пятый элемент после bswap
        }

        # Загружаем дамп памяти
        with open(self.memory_file, "r") as f:
            memory_dump = yaml.safe_load(f)

        # Сравниваем память
        for address, value in expected_memory.items():
            self.assertEqual(memory_dump[address], value)
