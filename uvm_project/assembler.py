
import struct
import yaml

class Assembler:
    def __init__(self, input_file, output_file, log_file=None):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        

    def assemble(self):
        with open(self.input_file, 'r') as f:
            lines = f.readlines()

        binary_data = bytearray()
        log_data = []

        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
                continue

            parts = line.split()
            mnemonic = parts[0]

            if mnemonic == 'LOAD':
                A = 82
                B = int(parts[1])
                C = int(parts[2])
                command = (A << 24) | (B << 12) | C
                binary_data.extend(command.to_bytes(4, byteorder='big'))
                log_data.append({'command': 'LOAD', 'A': A, 'B': B, 'C': C, 'binary': command})

            elif mnemonic == 'BSWAP':
                A = 22
                B = int(parts[1])
                C = int(parts[2])
                command = (A << 24) | (B << 12) | C
                binary_data.extend(command.to_bytes(4, byteorder='big'))
                log_data.append({'command': 'BSWAP', 'A': A, 'B': B, 'C': C, 'binary': command})

            elif mnemonic == 'READ':
                A = 19
                B = int(parts[1])
                C = int(parts[2])
                D = int(parts[3])
                command = (A << 40) | (B << 28) | (C << 16) | D
                binary_data.extend(command.to_bytes(6, byteorder='big'))
                log_data.append({'command': 'READ', 'A': A, 'B': B, 'C': C, 'D': D, 'binary': command})

            elif mnemonic == 'WRITE':
                A = 31
                B = int(parts[1])
                C = int(parts[2])
                D = int(parts[3])
                command = (A << 40) | (B << 28) | (C << 16) | D
                binary_data.extend(command.to_bytes(6, byteorder='big'))
                log_data.append({'command': 'WRITE', 'A': A, 'B': B, 'C': C, 'D': D, 'binary': command})

            else:
                raise ValueError(f"Unknown instruction: {mnemonic}")

        # Сохраняем бинарный файл
        with open(self.output_file, 'wb') as f:
            f.write(binary_data)

        # Сохраняем лог, если указан
        if self.log_file:
            with open(self.log_file, 'w') as f:
                yaml.dump(log_data, f, default_flow_style=False) 

