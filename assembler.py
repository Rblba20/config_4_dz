import json
import struct
import sys

# Команды УВМ с их описанием
COMMANDS = {
    'LOAD': {'opcode': 17, 'size': 3},
    'READ': {'opcode': 3, 'size': 2},
    'WRITE': {'opcode': 6, 'size': 4},
    '>=': {'opcode': 21, 'size': 4}
}


def assemble_instruction(line):
    # Собирает инструкцию в бинарный формат.
    parts = line.split()
    cmd = parts[0]
    if cmd not in COMMANDS:
        raise ValueError(f"Unknown command: {cmd}")

    opcode = COMMANDS[cmd]['opcode']
    size = COMMANDS[cmd]['size']
    args = list(map(int, parts[1:]))
    print(cmd)

    if cmd == 'LOAD':
        if len(args) != 3:
            raise ValueError(f"Invalid arguments for LOAD: {args}")
        a, b, c = args
        if not (0 <= a <= 31 and 0 <= b <= 7 and 0 <= c <= 0x1FFF):
            raise ValueError(f"Arguments out of range for LOAD: a={a}, b={b}, c={c}")
        opcode_byte = (a << 3) | b
        print(f"Assembling command: {cmd}, opcode: {opcode}, args: {args}")
        return struct.pack('<BH', opcode_byte, c)

    elif cmd == 'READ':
        if len(args) != 3:
            raise ValueError(f"Invalid arguments for READ: {args}")
        a, b, c = args
        if not (0 <= a <= 31 and 0 <= b <= 7 and 0 <= c <= 7):
            raise ValueError(f"Arguments out of range for READ: a={a}, b={b}, c={c}")
        opcode_byte = (a << 3) | b
        print(f"Assembling command: {cmd}, opcode: {opcode}, args: {args}")
        return struct.pack('<BB', opcode_byte, c)

    elif cmd == '>=':
        if len(args) != 3:
            raise ValueError(f"Invalid arguments for >=: {args}")
        a, b, c = args
        if not (0 <= a <= 31 and 0 <= b <= 0xFFFF and 0 <= c <= 7):
            raise ValueError(f"Arguments out of range for >=: a={a}, b={b}, c={c}")
        opcode_byte = (a << 3) | c  # Поле A (opcode) + младшие 3 бита от C
        print(f"Assembling command: {cmd}, opcode: {opcode}, args: {args}")
        return struct.pack('<BH', opcode_byte, b)

    elif cmd == 'WRITE':
        if len(args) != 3:
            raise ValueError(f"Invalid arguments for WRITE: {args}")
        a, b, c = args
        if not (0 <= a <= 31 and 0 <= b <= 0xFFFF and 0 <= c <= 7):
            raise ValueError(f"Arguments out of range for WRITE: a={a}, b={b}, c={c}")
        opcode_byte = (a << 3) | c  # Поле A (opcode) + младшие 3 бита от C
        print(f"Assembling command: {cmd}, opcode: {opcode}, args: {args}")
        return struct.pack('<BH', opcode_byte, b)

    else:
        raise ValueError(f"Unsupported command: {cmd}")


def assemble(input_file, output_file, log_file):
    # Ассемблирует программу.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_instructions = []
    log = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        binary = assemble_instruction(line)
        binary_instructions.append(binary)
        log.append({'instruction': line, 'binary': list(binary)})

    # Записываем бинарный файл
    with open(output_file, 'wb') as f:
        for instr in binary_instructions:
            f.write(instr)

    # Записываем лог
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=4)


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
# python assembler.py input.txt program.bin log.json
# python interpreter.py program.bin result.json 0 100