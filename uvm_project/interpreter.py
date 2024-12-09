
# -*- coding: utf-8 -*-
"""Интерпретатор виртуальной машины."""
import yaml
import struct
class Interpreter:
    
     
    
   def __init__(self, binary_file, memory_start, memory_end, output_file):
        self.binary_file = binary_file
        self.memory_start = memory_start
        self.memory_end = memory_end
        self.output_file = output_file
        self.memory = [0] * 1024  # УВМ имеет память размером 1024 ячейки
        self.instructions = []
        self.program_counter = 0

   def load_binary(self):
        """Загрузка бинарного файла в память инструкций."""
        with open(self.binary_file, 'rb') as f:
            binary_data = f.read()
        
        i = 0
        while i < len(binary_data):
            if len(binary_data) - i >= 6:  # Команда 6 байт
                instruction = int.from_bytes(binary_data[i:i+6], byteorder='big')
                self.instructions.append(instruction)
                i += 6
            elif len(binary_data) - i >= 4:  # Команда 4 байта
                instruction = int.from_bytes(binary_data[i:i+4], byteorder='big')
                self.instructions.append(instruction)
                i += 4
            else:
                raise ValueError("Неверный формат бинарного файла")

   def execute(self):
        """Исполнение команд в памяти инструкций."""
        while self.program_counter < len(self.instructions):
            instruction = self.instructions[self.program_counter]
            opcode = (instruction >> 24) & 0xFF  # Опкод (первые 8 бит)
            
            if opcode == 82:  # LOAD
                B = (instruction >> 12) & 0xFFF
                C = instruction & 0xFFF
                self.memory[B] = C

            elif opcode == 22:  # BSWAP
                B = (instruction >> 12) & 0xFFF
                C = instruction & 0xFFF
                value = self.memory[B]
                swapped = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)  # Обратный порядок байтов
                self.memory[C] = swapped

            elif opcode == 19:  # READ
                B = (instruction >> 28) & 0xFFF
                C = (instruction >> 16) & 0xFFF
                D = instruction & 0xFFFF
                address = self.memory[C] + D
                if 0 <= address < len(self.memory):
                    self.memory[B] = self.memory[address]
                else:
                    raise ValueError(f"READ: Недопустимый адрес {address}")

            elif opcode == 31:  # WRITE
                B = (instruction >> 28) & 0xFFF
                C = (instruction >> 16) & 0xFFF
                D = instruction & 0xFFFF
                address = self.memory[B] + C
                if 0 <= address < len(self.memory):
                    self.memory[address] = self.memory[D]
                else:
                    raise ValueError(f"WRITE: Недопустимый адрес {address}")

            else:
                raise ValueError(f"Неизвестная команда: {opcode}")

            self.program_counter += 1

   def dump_memory(self):
        """Сохранение памяти в диапазоне [memory_start, memory_end] в YAML-файл."""
        memory_dump = {
            "memory": self.memory[self.memory_start:self.memory_end + 1]
        }
        with open(self.output_file, 'w') as f:
            yaml.dump(memory_dump, f)

   def interpret(self):
        """Основной процесс интерпретации."""
        self.load_binary()
        self.execute()
        self.dump_memory()
