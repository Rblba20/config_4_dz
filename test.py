import json


# Определение виртуальной машины
class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size  # Массив памяти
        self.registers = [0] * 32  # 32 регистра

    def load_vector(self, vector, start_address):
        """Загрузить вектор в память"""
        for i, val in enumerate(vector):
            self.memory[start_address + i] = val
        print(f"Вектор загружен в память: {self.memory[start_address:start_address + len(vector)]}")

    def binary_operation_ge(self, vector_start_address, number, result_address, vector_length):
        """Поэлементная операция >= над вектором и числом"""
        for i in range(vector_length):
            # Операция ">=" между элементом вектора и числом
            if self.memory[vector_start_address + i] >= number:
                self.memory[result_address + i] = 1
            else:
                self.memory[result_address + i] = 0
        print(
            f"Результат операции '>=' записан в новый вектор: {self.memory[result_address:result_address + vector_length]}")

    def execute_program(self, vector, number, vector_length):
        # Адреса для вектора и результата
        vector_start_address = 0
        result_start_address = 100  # Можно использовать любую свободную область памяти

        # Загрузим вектор в память
        self.load_vector(vector, vector_start_address)

        # Выполним операцию ">=" поэлементно
        self.binary_operation_ge(vector_start_address, number, result_start_address, vector_length)


# Тестовые данные
vector = [10, 15, 8, 14, 19, 3, 14, 7]  # Входной вектор
number = 14  # Число, с которым будем сравнивать
vector_length = len(vector)  # Длина вектора

# Запуск виртуальной машины
vm = VirtualMachine()
vm.execute_program(vector, number, vector_length)

# Результаты выполнения программы (лог в формате JSON)
log = {
    "vector": vector,
    "number": number,
    "result_vector": vm.memory[100:100 + vector_length],
}

# Сохранение в файл логов в формате JSON
log_filename = "vm_log.json"
with open(log_filename, "w") as log_file:
    json.dump(log, log_file, indent=4)

print(f"Лог выполнения сохранен в {log_filename}")
