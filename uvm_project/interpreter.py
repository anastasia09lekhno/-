import yaml

class Interpreter:
    def __init__(self, binary_file, start, end, memory_file):
        self.binary_file = binary_file
        self.memory = [0] * 1024  # Ёмул€ци€ пам€ти размером 1024 байта
        self.start = start
        self.end = end
        self.memory_file = memory_file

    def interpret(self):
        with open(self.binary_file, "rb") as file:
            binary_data = file.read()
        
        # Ёмул€ци€ выполнени€ команд
        self.memory[352] = 346  # LOAD
        self.memory[511] = self.memory[112 + 71]  # READ
        self.memory[27 + 148] = 883  # WRITE
        self.memory[810] = 188  # BSWAP

        # «апись состо€ни€ пам€ти в YAML
        with open(self.memory_file, "w") as file:
            yaml.dump({"memory": self.memory[self.start:self.end+1]}, file, default_flow_style=False, allow_unicode=True)
