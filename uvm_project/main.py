import sys
from assembler import Assembler
from interpreter import Interpreter

def main():
    # Проверка аргументов командной строки
    if len(sys.argv) < 3:
        print("Использование:")
        print("  python main.py assembler <input.asm> <output.bin> [log.yaml]")
        print("  python main.py interpreter <binary_file> <memory_range> <output.yaml>")
        sys.exit(1)

    mode = sys.argv[1]  # Определяем режим: assembler или interpreter

    if mode == "assembler":
        # Для ассемблера передаются: исходный файл, бинарный файл, опционально лог
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        log_file = sys.argv[4] if len(sys.argv) > 4 else None

        assembler = Assembler(input_file, output_file, log_file)
        assembler.assemble()

    elif mode == "interpreter":
        # Для интерпретатора: бинарный файл, диапазон памяти, файл для дампа памяти
        binary_file = sys.argv[2]  # Путь к бинарному файлу
        memory_range = sys.argv[3]  # Диапазон памяти в формате "start-end"
        memory_file = sys.argv[4]   # Путь к файлу для дампа памяти

        # Разделение диапазона на start и end
        start, end = map(int, memory_range.split('-'))

        # Запуск интерпретатора
        interpreter = Interpreter(binary_file, start, end, memory_file)
        interpreter.interpret()

    else:
        print("Неверный режим. Используйте 'assembler' или 'interpreter'.")

if __name__ == "__main__":
    main()
