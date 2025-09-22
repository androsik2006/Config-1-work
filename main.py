#!/usr/bin/env python3
import os
import sys
import socket
import shlex


class UnixShellEmulator:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.environment_vars = os.environ.copy()
        self.is_running = True

        # Добавляем системные переменные
        self.environment_vars['USER'] = os.getenv('USER', 'user')
        self.environment_vars['HOME'] = os.getenv('HOME', '/home/user')
        self.environment_vars['PWD'] = self.current_directory

    def generate_prompt(self):
        """Генерация приглашения в формате username@hostname:path$"""
        try:
            username = self.environment_vars.get('USER', 'user')

            try:
                hostname = socket.gethostname()
            except:
                hostname = 'localhost'

            home_dir = self.environment_vars.get('HOME', '')
            display_path = self.current_directory

            if home_dir and self.current_directory.startswith(home_dir):
                display_path = '~' + self.current_directory[len(home_dir):]

            return f"{username}@{hostname}:{display_path}$ "

        except Exception as e:
            return "user@localhost:~$ "

    def parse_input(self, input_text):
        """Парсер ввода с раскрытием переменных окружения"""
        if not input_text or not input_text.strip():
            return []

        processed_text = input_text
        for var_name, var_value in self.environment_vars.items():
            placeholder = f"${var_name}"
            processed_text = processed_text.replace(placeholder, var_value)

        try:
            return shlex.split(processed_text)
        except ValueError:
            print("Ошибка: некорректный синтаксис команды")
            return []

    def handle_ls(self, args):
        """Обработка команды ls (заглушка)"""
        print("Команда: ls")
        if args:
            print(f"Аргументы: {' '.join(args)}")
        print("Реализация команды ls будет добавлена на следующих этапах")

    def handle_cd(self, args):
        """Обработка команды cd (заглушка)"""
        print("Команда: cd")
        if args:
            print(f"Аргументы: {' '.join(args)}")
        print("Реализация команды cd будет добавлена на следующих этапах")

    def handle_exit(self, args):
        """Обработка команды exit"""
        if args:
            print(f"Аргументы exit: {' '.join(args)}")
        print("Завершение работы эмулятора...")
        self.is_running = False

    def handle_unknown_command(self, command, args):
        """Обработка неизвестной команды"""
        print(f"Команда-заглушка: {command}")
        if args:
            print(f"Аргументы: {' '.join(args)}")

    def execute_command(self, tokens):
        """Выполнение команды"""
        if not tokens:
            return

        command = tokens[0]
        args = tokens[1:]

        try:
            if command == "ls":
                self.handle_ls(args)
            elif command == "cd":
                self.handle_cd(args)
            elif command == "exit":
                self.handle_exit(args)
            else:
                self.handle_unknown_command(command, args)

        except Exception as e:
            print(f"Ошибка выполнения команды '{command}': {e}")

    def demonstrate(self):
        """Демонстрация работы прототипа"""
        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ РАБОТЫ ПРОТОТИПА")
        print("=" * 60)

        # Тест 1: Основные команды
        print("\n1. ТЕСТ ОСНОВНЫХ КОМАНД:")
        print("─" * 40)
        self.execute_command(["ls"])
        print()
        self.execute_command(["cd", "/home/user"])
        print()
        self.execute_command(["unknown_cmd", "arg1", "arg2"])

        # Тест 2: Переменные окружения
        print("\n2. ТЕСТ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ:")
        print("─" * 40)
        test_input = 'echo Домашняя директория: $HOME, Пользователь: $USER'
        print(f"Ввод: {test_input}")
        tokens = self.parse_input(test_input)
        print(f"После раскрытия переменных: {tokens}")

        # Тест 3: Приглашение командной строки
        print("\n3. ТЕСТ ПРИГЛАШЕНИЯ КОМАНДНОЙ СТРОКИ:")
        print("─" * 40)
        print(f"Пример приглашения: {self.generate_prompt()}")

        # Тест 4: Обработка ошибок
        print("\n4. ТЕСТ ОБРАБОТКИ ОШИБОК:")
        print("─" * 40)
        try:
            test_input = 'ls -la "незакрытая кавычка'
            print(f"Ввод с ошибкой: {test_input}")
            tokens = self.parse_input(test_input)
            print("Ошибка gracefully handled")
        except Exception as e:
            print(f"Перехвачена ошибка: {e}")

        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА. ЗАПУСКАЕМ ИНТЕРАКТИВНЫЙ РЕЖИМ...")
        print("=" * 60)

    def run(self):
        """Главный цикл REPL"""
        self.demonstrate()

        print("Добро пожаловать в эмулятор UNIX-оболочки!")
        print("Доступные команды: ls, cd, exit")
        print("Поддержка переменных окружения: $HOME, $USER, $PWD")
        print("Для выхода введите 'exit' или Ctrl+D")
        print("─" * 60)

        while self.is_running:
            try:
                prompt = self.generate_prompt()
                user_input = input(prompt).strip()

                if not user_input:
                    continue

                tokens = self.parse_input(user_input)
                if tokens:
                    self.execute_command(tokens)

            except EOFError:  # Ctrl+D
                print("\nЗавершение работы...")
                break
            except KeyboardInterrupt:  # Ctrl+C
                print("\nДля выхода используйте 'exit'")
                continue
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                break


def main():
    """Точка входа"""
    shell = UnixShellEmulator()
    shell.run()


if __name__ == "__main__":
    main()
