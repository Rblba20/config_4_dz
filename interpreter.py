import json
import struct
import sys


def execute_program(binary_file, result_file, memory_range):
    # Выполняет программу из бинарного файла.
    memory = [0] * 1024  # Пример памяти
    registers = [0] * 8  # Пример регистров

    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    pc = 0
    while pc < len(binary_data):
        byte = binary_data[pc]
        opcode = (byte >> 3) & 0x1F
        #print(f"PC={pc}, Opcode={opcode}, Byte={byte}, Full instruction: {binary_data[pc:pc + 4].hex()}")
        if opcode == 17:  # LOAD
            b = byte & 0x07
            c = struct.unpack_from('<H', binary_data, pc + 1)[0]
            print(f"LOAD: Register {b} <- {c}")
            registers[b] = c
            pc += 3

        elif opcode == 3:  # READ
            b = byte & 0x07
            c = binary_data[pc + 1]
            print(f"READ: {b} <- Register {c}")
            registers[b] = memory[c]
            pc += 2

        # elif opcode == 6:  # WRITE
        #     b = struct.unpack_from('<H', binary_data, pc + 1)[0]  # Адрес памяти
        #     c = binary_data[pc + 3] & 0x07  # Номер регистра
        #     print(f"WRITE: Memory[{b}] <- Register {c}")
        #     memory[b] = registers[c]
        #     pc += 4

        elif opcode == 6:  # WRITE
            b = struct.unpack_from('<H', binary_data, pc + 1)[0]  # Адрес памяти (16 бит)
            c = byte & 0x07  # Номер регистра (младшие 3 бита от opcode_byte)
            print(f"WRITE: Memory[{b}] <- Register {c}")
            memory[b] = registers[c]
            pc += 3


        # elif opcode == 21:  # >=
        #     b = struct.unpack_from('<H', binary_data, pc + 1)[0]  # Адрес памяти
        #     c = binary_data[pc + 3] & 0x07  # Регистр для результата
        #     print(f">=: Register {c} <- (Register {c} >= Memory[{b}])")
        #     registers[c] = int(registers[c] >= memory[b])
        #     pc += 4

        # elif opcode == 21:  # >=
        #     b = struct.unpack_from('<H', binary_data, pc + 1)[0]  # Адрес памяти (16 бит)
        #     c = byte & 0x07  # Номер регистра (младшие 3 бита от opcode_byte)
        #     print(f">=: Register {c} <- (Register {c} >= Memory[{b}])")
        #     registers[c] = int(registers[c] >= memory[b])
        #     pc += 4

        elif opcode == 21:  # >=
            b = struct.unpack_from('<H', binary_data, pc + 1)[0]  # Адрес памяти (16 бит)
            c = byte & 0x07  # Номер регистра (младшие 3 бита от opcode_byte)
            print(f">=: Register {c} <- (Register {c} >= Memory[{b}])")
            registers[c] = int(registers[c] >= memory[b])
            # print(registers[c])
            # print(memory[b])
            # print(int(registers[c] >= memory[b]))
            pc += 3
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    # Сохраняем результаты
    # result = {i: memory[i] for i in range(*memory_range)}
    # reg = {i: registers[i] for i in range(len(registers))}
    # with open(result_file, 'w') as f:
    #     json.dump(result, f, indent=4)
    #     json.dump(reg, f, indent=4)
    result = {i: memory[i] for i in range(*memory_range)}
    reg = {i: registers[i] for i in range(len(registers))}

    # Объединяем оба словаря в один
    output_data = {
        "result": result,
        "registers": reg
    }

    # Записываем объединенный словарь в JSON файл
    with open(result_file, 'w') as f:
        json.dump(output_data, f, indent=4)


if __name__ == '__main__':
    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    memory_range = tuple(map(int, sys.argv[3:5]))
    #print(binary_file, result_file, memory_range)
    execute_program(binary_file, result_file, memory_range)
