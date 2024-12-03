import unittest
from assembler import Assembler
import os
import yaml

class TestAssembler(unittest.TestCase):
    def setUp(self):
        """Создание временных файлов для тестов."""
        self.input_asm = "tests/temp_input.asm"
        self.output_bin = "tests/temp_output.bin"
        self.log_file = "tests/temp_log.yaml"

    def tearDown(self):
        """Удаление временных файлов после тестов."""
        for file in [self.input_asm, self.output_bin, self.log_file]:
            if os.path.exists(file):
                os.remove(file)

    def write_to_file(self, filename, content):
        """Записывает текстовое содержимое в файл."""
        with open(filename, 'w') as f:
            f.write(content)

    def test_load_instruction(self):
        asm_code = "LOAD 352, 346"
        self.write_to_file(self.input_asm, asm_code)

        assembler = Assembler(self.input_asm, self.output_bin, self.log_file)
        assembler.assemble()

        with open(self.output_bin, "rb") as f:
            binary = f.read()
        self.assertEqual(binary, bytes([0x52, 0xB0, 0xD0, 0x0A]))

        with open(self.log_file, "r") as f:
            log = yaml.safe_load(f)
        self.assertEqual(log, [{"command": "LOAD", "B": 352, "C": 346}])

    def test_bswap_instruction(self):
        asm_code = "BSWAP 810, 188"
        self.write_to_file(self.input_asm, asm_code)

        assembler = Assembler(self.input_asm, self.output_bin, self.log_file)
        assembler.assemble()

        with open(self.output_bin, "rb") as f:
            binary = f.read()
        self.assertEqual(binary, bytes([0x16, 0x95, 0xE1, 0x05]))

        with open(self.log_file, "r") as f:
            log = yaml.safe_load(f)
        self.assertEqual(log, [{"command": "BSWAP", "B": 810, "C": 188}])

    def test_read_instruction(self):
        asm_code = "READ 511, 112, 71"
        self.write_to_file(self.input_asm, asm_code)

        assembler = Assembler(self.input_asm, self.output_bin, self.log_file)
        assembler.assemble()

        with open(self.output_bin, "rb") as f:
            binary = f.read()
        self.assertEqual(binary, bytes([0x93, 0xFF, 0x80, 0x83, 0x23, 0x00]))

        with open(self.log_file, "r") as f:
            log = yaml.safe_load(f)
        self.assertEqual(log, [{"command": "READ", "B": 511, "C": 112, "D": 71}])

    def test_write_instruction(self):
        asm_code = "WRITE 27, 148, 883"
        self.write_to_file(self.input_asm, asm_code)

        assembler = Assembler(self.input_asm, self.output_bin, self.log_file)
        assembler.assemble()

        with open(self.output_bin, "rb") as f:
            binary = f.read()
        self.assertEqual(binary, bytes([0x9F, 0x0D, 0xA0, 0x64, 0x6E, 0x00]))

        with open(self.log_file, "r") as f:
            log = yaml.safe_load(f)
        self.assertEqual(log, [{"command": "WRITE", "B": 27, "C": 148, "D": 883}])

if __name__ == "__main__":
    unittest.main()
