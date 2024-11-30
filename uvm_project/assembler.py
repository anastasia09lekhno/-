
import struct
import yaml

class Assembler:
    def __init__(self, input_file, output_file, log_file=None):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        self.commands = []

    def assemble(self):
        with open(self.input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Пропускаем комментарии и пустые строки

            command = self.parse_command(line)
            self.commands.append(command)

        # Сохраняем бинарный файл
        with open(self.output_file, 'wb') as f:
            for cmd in self.commands:
                f.write(cmd['binary'])

        # Логируем команды
        if self.log_file:
            with open(self.log_file, 'w') as f:
                yaml.dump(self.commands, f)

    def parse_command(self, line):
        parts = line.split()
        mnemonic = parts[0]

        if mnemonic == "LOAD":
            a = int(parts[1])
            b = int(parts[2])
            c = int(parts[3])
            binary = ((a & 0x7F) << 25) | ((b & 0xFFF) << 13) | (c & 0x3FF)
            return {
                "mnemonic": "LOAD",
                "A": a,
                "B": b,
                "C": c,
                "binary": binary.to_bytes(4, 'big')
            }
        elif mnemonic == "BSWAP":
            a = int(parts[1])
            b = int(parts[2])
            c = int(parts[3])
            binary = ((a & 0x7F) << 25) | ((b & 0xFFF) << 13) | ((c & 0xFFF) << 1)
            return {
                "mnemonic": "BSWAP",
                "A": a,
                "B": b,
                "C": c,
                "binary": binary.to_bytes(4, 'big')
            }
        else:
            raise ValueError(f"Неизвестная команда: {mnemonic}")
   

