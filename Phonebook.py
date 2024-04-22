# Функция запрашивает у пользователя информацию о новом контакте
def ask_data():
    return {
        'second_name' : input("Введите фамилию: "),
        'first_name'  : input("Введите имя: "),
        'middle_name' : input("Введите отчество: "),
        'phone_number': input("Введите номер телефона: ")
    }

# Запрашиваем данные о новом контакте
def add_new_contact():  
    contact = ask_data()
    # Проверяем, что все поля заполнены
    if all(contact.values()):
        
        # Проверяем наличие файла назначения и создаем его, если он отсутствует
        try:
            with open('phonebook.txt', 'x', encoding='utf-8'):
                pass  # Просто создаем файл, если его нет
        except FileExistsError:
            pass  # Файл уже существует
        
        # Считываем содержимое файла в список строк
        with open('phonebook.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # Определяем номер строки для записи нового контакта
        line_number = len(lines) + 1
        # Записываем новый контакт в файл
        with open('phonebook.txt', 'a', encoding='utf-8') as file:
            file.write(f"{line_number};{';'.join(contact.values())}\n")
        print('Контакт записан!')

# Открываем телефонную книгу и выводим ее содержимое на экран
def open_phonebook():
    with open('phonebook.txt', 'r', encoding='utf-8') as file:
        title = ["№ п\п", "Фамилия", "Имя", "Отчество", "Телефон"]
        print("-" * (len(title) * 18 + 1))
        print("| {} |".format(" | ".join("{:<15}".format(t) for t in title)))
        print("-" * (len(title) * 18 + 1))
        for line in file:
            contact_info = line.strip().split(';')
            print("| {} |".format(" | ".join("{:<15}".format(info) for info in contact_info)))
        print("-" * (len(title) * 18 + 1))

# Функция для поиска контактов в телефонной книге
def find_contact():
    search_option = int(input("Выберите вариант поиска:\n1. По номеру строки\n2. По фамилии\n3. По имени\n4. По отчеству\n5. По номеру телефона\n>  "))
    search_query = input("Введите поисковой запрос: ").lower()
    
    found_contacts = []
    # Открываем файл и ищем соответствующие контакты
    with open('phonebook.txt', 'r', encoding='utf-8') as file:
        for line in file:
            contact_info = line.rstrip('\n').split(';')
            if search_option == 1 and search_query in contact_info[0]:  # Поиск по номеру строки
                found_contacts.append(contact_info)
            elif search_option == 2 and search_query in contact_info[1].lower():  # Поиск по фамилии
                found_contacts.append(contact_info)
            elif search_option == 3 and search_query in contact_info[2].lower():  # Поиск по имени
                found_contacts.append(contact_info)
            elif search_option == 4 and search_query in contact_info[3].lower():  # Поиск по отчеству
                found_contacts.append(contact_info)
            elif search_option == 5 and search_query in contact_info[4]:  # Поиск по номеру телефона
                found_contacts.append(contact_info)
                
    if found_contacts:
        # Если найдены контакты, выводим их на экран
        title = ["№ п\п", "Фамилия", "Имя", "Отчество", "Телефон"]
        print("-" * (len(title) * 18 + 1))
        print("| {} |".format(" | ".join("{:<15}".format(t) for t in title)))
        print("-" * (len(title) * 18 + 1))        
        for contact in found_contacts:
            print("| {} |".format(" | ".join("{:<15}".format(info) for info in contact)))
        print("-" * (len(title) * 18 + 1))
    else:
        # Если контакты не найдены, выводим сообщение об этом
        print("Контакты не найдены.")
    
    return found_contacts

# Функция для удаления контактов из телефонной книги
def delete_contact():
    print("Найденные контакты:")
    found_contacts = find_contact()
    
    if not found_contacts:
        # Если контакт не найден, сообщаем об этом и выходим из функции
        print("Контакт не найден! Удаление невозможно!")
        return
    
    confirm_delete = input("Вы уверены, что хотите удалить найденные контакты? (да/нет): ")
    if confirm_delete.lower() == 'да':
        # Создаем список строк, которые нужно оставить в файле
        lines_to_keep = []
        with open('phonebook.txt', 'r', encoding='utf-8') as file:
            for line in file:
                contact_info = line.strip().split(';')
                if contact_info in found_contacts:
                    continue
                lines_to_keep.append(';'.join(contact_info[1:]))
        # Перезаписываем файл с обновленными строками
        with open('phonebook.txt', 'w', encoding='utf-8') as file:
            for line_number, line in enumerate(lines_to_keep, 1):
                file.write(f"{line_number};{line}\n")
        print("Контакты успешно удалены!")        

# Функция для копирования контактов из телефонной книги в другой файл       
def copy_contact():
    found_contacts = find_contact()
    if not found_contacts:
        # Если контакт не найден, сообщаем об этом и выходим из функции
        print("Контакт не найден. Копирование невозможно!")
        return
    
    confirm_copy = input("Вы уверены, что хотите скопировать найденные контакты? (да/нет): ")
    if confirm_copy.lower() == 'да':
        destination_file = input("Введите имя файла, куда скопировать контакты: ")
        
        # Проверяем наличие файла назначения и создаем его, если он отсутствует
        try:
            with open(destination_file, 'x', encoding='utf-8'):
                pass  # Просто создаем файл, если его нет
        except FileExistsError:
            pass  # Файл уже существует
        
        # Считываем содержимое файла назначения
        with open(destination_file, 'r', encoding='utf-8') as copy_file:
            existing_lines = copy_file.readlines()
        
        # Определяем номер строки для записи новых контактов в файле назначения
        if existing_lines:
            last_line_number = int(existing_lines[-1].split(';')[0])
        else:
            last_line_number = 0
        
        # Записываем новые контакты в файл с учетом существующих записей
        with open(destination_file, 'a', encoding='utf-8') as copy_file:
            for contact in found_contacts:
                copy_file.write(f"{last_line_number + 1};{';'.join(contact[1:])}\n")
                last_line_number += 1
        
        print("Контакты успешно скопированы!")

# Функция для изменения контактов в телефонной книге
def edit_contact():
    print("Найденные контакты:")
    found_contacts = find_contact()
    
    if not found_contacts:
        # Если контакт не найден, сообщаем об этом и выходим из функции
        print("Контакт не найден! Изменение невозможно!")
        return
    
    confirm_edit = input("Вы уверены, что хотите изменить найденные контакты? (да/нет): ")
    if confirm_edit.lower() == 'да':    
        # Создаем список для хранения измененных контактов
        updated_contacts = []
        for contact in found_contacts:
            print("Текущая информация о контакте:", contact)
            updated_contact = ask_data()
            # Обновляем найденный контакт информацией, введенной пользователем
            contact[1:] = updated_contact.values()
            updated_contacts.append(contact)
        
        # Считываем содержимое файла в список строк
        with open('phonebook.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Обновляем строки файла с информацией о контактах
        for contact_info in updated_contacts:
            for i, line in enumerate(lines):
                if line.startswith(contact_info[0]):
                    lines[i] = f"{contact_info[0]};{';'.join(contact_info[1:])}\n"
                    break
        
        # Перезаписываем файл с обновленными строками
        with open('phonebook.txt', 'w', encoding='utf-8') as file:
            file.writelines(lines)
        
        print("Контакты успешно изменены!")
        

# Основная функция (меню), управляющая всей программой
def main():
    while True:
        actions = {
            1: find_contact,
            2: add_new_contact,
            3: delete_contact,
            4: open_phonebook,
            5: copy_contact,
            6: edit_contact,
            0: exit
        }
        is_stop = int(input("Выберете действие:\n1. Найти\n2. Добавить\n3. Удалить\n4. Просмотреть книгу\n5. Копирование контактов\n6. Изменить контакт\n0. Выход\n>  "))
        action = actions.get(is_stop)
        if action:
            action()
        else:
            print("Некорректный ввод, попробуйте еще раз.")
        input("Нажмите Enter чтобы продолжить")

# Вызов основной функции (меню)
main()