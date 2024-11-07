import os
import heapq
import json
from collections import Counter

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def create_huffman_codes(node, prefix="", codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        create_huffman_codes(node.left, prefix + "0", codebook)
        create_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text, codebook):
    return ''.join(codebook[char] for char in text)

def huffman_decode(encoded_bytes, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    bits = ''.join(f'{byte:08b}' for byte in encoded_bytes)
    decoded_text = ""
    current_code = ""
    
    for bit in bits:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text += reverse_codebook[current_code]
            current_code = ""
    
    return decoded_text

class ShannonFanoNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq

def shannon_fano_codebook(frequency):
    def build_codebook(symbols):
        if len(symbols) == 1:
            return {symbols[0].char: ""}

        total = sum(symbol.freq for symbol in symbols)
        cumulative = 0
        split_index = 0

        for i, symbol in enumerate(symbols):
            cumulative += symbol.freq
            if cumulative >= total / 2:
                split_index = i + 1
                break

        left = symbols[:split_index]
        right = symbols[split_index:]

        codebook = {}
        for char, code in build_codebook(left).items():
            codebook[char] = "0" + code
        for char, code in build_codebook(right).items():
            codebook[char] = "1" + code

        return codebook

    symbols = [ShannonFanoNode(char, freq) for char, freq in frequency.items()]
    return build_codebook(sorted(symbols, key=lambda x: x.freq, reverse=True))

def shannon_fano_encode(text, codebook):
    return ''.join(codebook[char] for char in text)

def shannon_fano_decode(encoded_bytes, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    bits = ''.join(f'{byte:08b}' for byte in encoded_bytes)
    decoded_text = ""
    current_code = ""
    
    for bit in bits:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text += reverse_codebook[current_code]
            current_code = ""
    
    return decoded_text

def bits_to_bytes(bits):
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            byte = byte.ljust(8, '0')
        byte_array.append(int(byte, 2))
    return byte_array

def write_encoded_to_file(encoded_bytes, output_file):
    with open(output_file, 'wb') as file:
        file.write(encoded_bytes)

def save_codebook_to_json(codebook, json_file):
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(codebook, file, ensure_ascii=False, indent=4)

def huffman_compress_to_file(input_file, output_file, json_file, input_encoding):
    with open(input_file, 'r', encoding=input_encoding) as file:
        text = file.read()

    frequency = Counter(text)
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = create_huffman_codes(huffman_tree)
    encoded_text = huffman_encode(text, huffman_codes)
    encoded_bytes = bits_to_bytes(encoded_text)

    write_encoded_to_file(encoded_bytes, output_file)
    save_codebook_to_json(huffman_codes, json_file)

    print(f"Сжатый текст записан в файл: {output_file}")
    print(f"Кодовая таблица сохранена в JSON файл: {json_file}")

def shannon_fano_compress_to_file(input_file, output_file, json_file, input_encoding):
    with open(input_file, 'r', encoding=input_encoding) as file:
        text = file.read()

    frequency = Counter(text)
    shannon_fano_codes = shannon_fano_codebook(frequency)
    encoded_text = shannon_fano_encode(text, shannon_fano_codes)
    encoded_bytes = bits_to_bytes(encoded_text)

    write_encoded_to_file(encoded_bytes, output_file)
    save_codebook_to_json(shannon_fano_codes, json_file)

    print(f"Сжатый текст записан в файл: {output_file}")
    print(f"Кодовая таблица сохранена в JSON файл: {json_file}")

def decompress_from_file(encoded_file, json_file, output_file, algorithm):
    with open(encoded_file, 'rb') as file:
        encoded_bytes = file.read()

    with open(json_file, 'r', encoding='utf-8') as file:
        codebook = json.load(file)

    if algorithm == 'huffman':
        decoded_text = huffman_decode(encoded_bytes, codebook)
    elif algorithm == 'shannon_fano':
        decoded_text = shannon_fano_decode(encoded_bytes, codebook)
    else:
        raise ValueError("Неверный алгоритм. Выберите 'huffman' или 'shannon_fano'.")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(decoded_text)

    print(f"Декодированный текст записан в файл: {output_file}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_algorithm_choice():
    print("Выберите алгоритм:")
    print("1. Алгоритм Хаффмана")
    print("2. Алгоритм Шеннона-Фано")
    choice = input("Введите цифру: ").strip()
    return 'huffman' if choice == '1' else 'shannon_fano'

if __name__ == "__main__":
    clear_console()
    action = input("Введите 'c' для сжатия или 'd' для декодирования: ").strip().lower()
    
    if action == 'c':
        algorithm = get_algorithm_choice()
        input_file = input("Введите название файла для кодирования (с расширением): ").strip()
        output_file = input("Введите название файла для сжатого текста (с расширением): ").strip()
        json_file = input("Введите название файла для кодовой таблицы (с расширением .json): ").strip()
        input_encoding = input("Введите кодировку файла (например, utf-8): ").strip()

        if algorithm == 'huffman':
            huffman_compress_to_file(input_file, output_file, json_file, input_encoding)
        else:
            shannon_fano_compress_to_file(input_file, output_file, json_file, input_encoding)

    elif action == 'd':
        algorithm = get_algorithm_choice()
        encoded_file = input("Введите название файла с сжатым текстом (с расширением): ").strip()
        json_file = input("Введите название JSON файла с кодовой таблицей (с расширением .json): ").strip()
        output_file = input("Введите название файла для декодированного текста (с расширением): ").strip()

        decompress_from_file(encoded_file, json_file, output_file, algorithm)
    
    else:
        print("Неверное действие. Введите 'c' для сжатия или 'd' для декодирования.")
