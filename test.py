import unittest
import subprocess
import json
import os


class TestAssemblerAndInterpreter(unittest.TestCase):
    def setUp(self):
        """Создаем файл input.txt для теста."""
        self.input_file = 'input.txt'
        self.binary_file = 'program.bin'
        self.log_file = 'log.json'
        self.result_file = 'result.json'

        # Содержимое input.txt
        input_data = """\
LOAD 17 0 23
LOAD 17 1 12
LOAD 17 2 2
LOAD 17 3 56
LOAD 17 4 89
LOAD 17 5 90
LOAD 17 6 15
LOAD 17 7 8

WRITE 6 0 0
WRITE 6 1 1
WRITE 6 2 2
WRITE 6 3 3
WRITE 6 4 4
WRITE 6 5 5
WRITE 6 6 6
WRITE 6 7 7

LOAD 17 0 14
LOAD 17 1 14
LOAD 17 2 14
LOAD 17 3 14
LOAD 17 4 14
LOAD 17 5 14
LOAD 17 6 14
LOAD 17 7 14

>= 21 0 0
>= 21 1 1
>= 21 2 2
>= 21 3 3
>= 21 4 4
>= 21 5 5
>= 21 6 6
>= 21 7 7

WRITE 6 0 0
WRITE 6 1 1
WRITE 6 2 2
WRITE 6 3 3
WRITE 6 4 4
WRITE 6 5 5
WRITE 6 6 6
WRITE 6 7 7
"""
        with open(self.input_file, 'w') as f:
            f.write(input_data)

    def test_assembler_and_interpreter(self):
        """Тестируем работу assembler.py и interpreter.py."""
        # Шаг 1: Запускаем assembler.py
        subprocess.run(
            ['python', 'assembler.py', self.input_file, self.binary_file, self.log_file],
            check=True
        )

        # Проверяем, что бинарный файл был создан
        self.assertTrue(os.path.exists(self.binary_file))

        # Шаг 2: Запускаем interpreter.py
        memory_range = (0, 8)  # Диапазон памяти для проверки
        subprocess.run(
            ['python', 'interpreter.py', self.binary_file, self.result_file, str(memory_range[0]), str(memory_range[1])],
            check=True
        )

        # Проверяем, что файл результата был создан
        self.assertTrue(os.path.exists(self.result_file))

        # Шаг 3: Проверяем содержимое файла результата
        with open(self.result_file, 'r') as f:
            result = json.load(f)

        # Ожидаемый результат в памяти (после выполнения >=)
        expected_memory = {
            "0": 0,
            "1": 1,
            "2": 1,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 1
        }

        # Проверяем соответствие памяти
        self.assertEqual(result['result'], expected_memory)

        # Проверяем, что регистры также установлены корректно
        expected_registers = {
            "0": 0,
            "1": 1,
            "2": 1,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 1
        }
        self.assertEqual(result['registers'], expected_registers)


if __name__ == '__main__':
    unittest.main()
