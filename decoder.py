import chardet
import os

# Функция для определения кодировки файла
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        detector = chardet.detect(data)
        encoding = detector['encoding']
        return encoding

# Функция для преобразования кодировки файла
def convert_encoding(input_file, output_file, target_encoding):
    try:
        source_encoding = detect_encoding(input_file)
        if not source_encoding:
            print(f"Не удалось определить кодировку для файла {input_file}.")
            return
        
        with open(input_file, 'r', encoding=source_encoding) as input_file:
            content = input_file.read()
        
        with open(output_file, 'w', encoding=target_encoding) as output:
            output.write(content)
        
        print(f"Файл успешно преобразован в кодировку {target_encoding}. Сохранен как '{output_file}'.")
    except Exception as e:
        print(f"Ошибка: {e}")

# Очистка консоли для удобства
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Функция для создания файла с заданной кодировкой
def create_file_with_encoding(file_path, content, encoding):
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)
        print(f"Файл '{file_path}' успешно создан с кодировкой {encoding}.")
    except Exception as e:
        print(f"Ошибка: {e}")

# Основная функция программы
def main():
    clear_console()

    print("Что вы хотите сделать?")
    print(" 1. Создать файл с определенной кодировкой\n 2. Определить и изменить кодировку файла\n")
    
    choice = input("Выбор: ")
    
    encoding_map = {'1': 'CP866', '2': 'CP1251', '3': 'maccyrillic', '4': 'ISO-8859-5'}

    if choice == '1':
        # Режим создания файла
        file_path = input("Введите имя файла для создания: ")
        content = input("Введите текст для файла: ")
        
        print("Выберите кодировку для создания файла:")
        print(" 1. CP866\n 2. CP1251\n 3. maccyrillic\n 4. ISO-8859-5\n")
        encoding_choice = input("Выбор: ")
        target_encoding = encoding_map.get(encoding_choice)
        
        if target_encoding is None:
            print("Ошибка: неправильный выбор кодировки.")
        else:
            create_file_with_encoding(file_path, content, target_encoding)
        return  # Завершаем работу после создания файла
    
    elif choice == '2':
        # Режим определения и изменения кодировки
        file_path = input("Введите полный путь к файлу для изменения кодировки: ")
        encoding = detect_encoding(file_path)
        
        if encoding:
            print(f"Текущая кодировка файла: {encoding}")
        
        print("Выберите кодировку для преобразования:")
        print(" 1. CP866\n 2. CP1251\n 3. maccyrillic\n 4. ISO-8859-5\n")
        encoding_choice = input("Выбор: ")
        target_encoding = encoding_map.get(encoding_choice)
        
        if target_encoding is None:
            print("Ошибка: неправильный выбор кодировки.")
        else:
            output_file_path = input("Введите имя для выходного файла: ")
            convert_encoding(file_path, output_file_path, target_encoding)
    
    else:
        print("Ошибка: неправильный выбор действия.")

if __name__ == "__main__":
    main()
