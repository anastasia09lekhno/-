import os
import zipfile
import argparse
import tkinter as tk
from tkinter import scrolledtext
import xml.etree.ElementTree as ET
import time


class ShellEmulator:
    def __init__(self, username, zip_path, log_path):
        self.username = username
        self.zip_path = zip_path
        self.log_path = log_path

        # Инициализация корня файловой системы
        self.fs_root = os.path.join(os.path.dirname(__file__), "virtual_fs")

        # Создаем директорию для виртуальной файловой системы, если её нет
        if not os.path.exists(self.fs_root):
            os.mkdir(self.fs_root)

        # Текущая директория - начнем с корня виртуальной файловой системы
        self.current_directory = self.fs_root

        # Загружаем ZIP-файл в виртуальную файловую систему
        self.load_zip(zip_path)

        # Лог действий пользователя
        self.log_actions = []

    def load_zip(self, zip_path):
        """Загружаем и разархивируем ZIP-файл в виртуальную файловую систему"""
        # Проверяем существование виртуальной файловой системы и распаковываем архив
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.fs_root)

    def ls(self):
        """Команда ls - вывод списка файлов и директорий"""
        try:
            files = os.listdir(self.current_directory)
            if files:
                return "\n".join(files)
            else:
                return "No files or directories found."
        except FileNotFoundError:
            return "Directory not found."

    def cd(self, path):
        """Команда cd - смена директории"""
        new_dir = os.path.join(self.current_directory, path)
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            self.current_directory = new_dir
            return f"Changed directory to {new_dir}"
        else:
            return f"Directory not found: {path}"

    def cat(self, filename):
        """Команда cat - вывод содержимого файла"""
        file_path = os.path.join(self.current_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return f"File not found: {filename}"

    def rm(self, filename):
        """Команда rm - удаление файла"""
        file_path = os.path.join(self.current_directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"File {filename} deleted."
        else:
            return f"File not found: {filename}"

    def exit(self):
        """Команда exit - выход из программы"""
        self.save_log()
        return "Exiting shell."

    def log(self, action):
        """Логирование действий пользователя"""
        self.log_actions.append({
            "user": self.username,
            "action": action,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    def save_log(self):
        """Сохранение лога в XML файл"""
        root = ET.Element("log")
        for entry in self.log_actions:
            action_element = ET.SubElement(root, "action")
            user_element = ET.SubElement(action_element, "user")
            user_element.text = entry["user"]
            action_element.text = entry["action"]
            timestamp_element = ET.SubElement(action_element, "timestamp")
            timestamp_element.text = entry["timestamp"]

        tree = ET.ElementTree(root)
        tree.write(self.log_path)


class ShellGUI:
    def __init__(self, shell):
        self.shell = shell
        self.window = tk.Tk()
        self.window.title(f"Shell Emulator - {shell.username}")

        # Создание интерфейса
        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        self.entry = tk.Entry(self.window)
        self.entry.pack(fill='x')
        self.entry.bind("<Return>", self.on_enter)

    def on_enter(self, event):
        """Обработка ввода команд"""
        command = self.entry.get()
        self.shell.log(command)
        self.entry.delete(0, tk.END)
        output = self.execute_command(command)
        self.text_area.insert(tk.END, f"{self.shell.username}@shell> {command}\n{output}\n")

    def execute_command(self, command):
        """Выполнение команд"""
        if command.startswith("ls"):
            return self.shell.ls()
        elif command.startswith("cd"):
            path = command.split(" ")[1]
            return self.shell.cd(path)
        elif command.startswith("cat"):
            filename = command.split(" ")[1]
            return self.shell.cat(filename)
        elif command.startswith("rm"):
            filename = command.split(" ")[1]
            return self.shell.rm(filename)
        elif command == "exit":
            return self.shell.exit()
        else:
            return "Unknown command"

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # Код выполняется только если программа запущена напрямую
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--username", required=True, help="Username for the shell prompt")
    parser.add_argument("--zip_path", required=True, help="Path to the virtual file system (zip archive)")
    parser.add_argument("--log_path", required=True, help="Path to the log file (xml format)")
    args = parser.parse_args()

    # Запуск эмулятора
    shell = ShellEmulator(args.username, args.zip_path, args.log_path)
    gui = ShellGUI(shell)
    gui.run()
