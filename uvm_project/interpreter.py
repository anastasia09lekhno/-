import yaml

class Interpreter:
    def __init__(self, binary_file, start, end, output_file):
        self.binary_file = binary_file
        self.start = start
        self.end = end
        self.output_file = output_file
        self.memory = [0] * 1024

    def interpret(self):
        with open(self.binary_file, 'rb') as f:
            binary_data = f.read()

        pc = 0  # Программный счетчик
        while pc < len(binary_data):
            command = binary_data[pc:pc + 4]
            pc += 4
            self.execute_command(command)

        self.dump_memory()

    def execute_command(self, command):
        opcode = (command[0] & 0xFC) >> 2
        if opcode == 82:  # LOAD
            addr = ((command[0] & 0x3) << 10) | (command[1] << 2) | (command[2] >> 6)
            value = ((command[2] & 0x3F) << 8) | command[3]
            self.memory[addr] = value
        elif opcode == 22:  # BSWAP
            addr_src = ((command[0] & 0x3) << 10) | (command[1] << 2) | (command[2] >> 6)
            addr_dest = ((command[2] & 0x3F) << 8) | command[3]
            value = self.memory[addr_src]
            swapped = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
            self.memory[addr_dest] = swapped
        else:
            raise ValueError(f"Неизвестный opcode: {opcode}")

    def dump_memory(self):
        memory_dump = {f"address_{i}": self.memory[i] for i in range(self.start, self.end + 1)}
        with open(self.output_file, 'w') as f:
            yaml.dump(memory_dump, f)
