from pprint import pprint
import csv
import re

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding='utf-8') as file:
    rows = csv.reader(file, delimiter=",")
    contacts_list = list(rows)

# Форматируем полные имена
phone_book = []
full_name_pattern = r'(^[А-Я]\w+) ?,?(\w+) ?,?(\w+)?'
substitution_full_name_pattern = r'\1,\2,\3'
for contact_info in contacts_list:
    while '' in contact_info:
        contact_info.remove('')
    result = re.sub(full_name_pattern, substitution_full_name_pattern, ','.join(contact_info))
    phone_book.append(result)

# Форматируем номера телефонов
phone_number_pattern = r'(\+7|8) ?\(?(\d{3})\)?-? ?(\d{3})\-? ?(\d{2})-? ?(\d{2}) ?\(?(доб\.)? ?(\d+)?(\))?'
substitution_phone_number_pattern = r'+7(\2)\3-\4-\5 \6\7'
for index, contact in enumerate(phone_book):
    contact_info = contact.split(',')
    result = re.sub(phone_number_pattern, substitution_phone_number_pattern, ','.join(contact_info))
    phone_book[index] = result

phone_book_dict = {}
for entry in phone_book:
    if list(phone_book_dict.keys()).count(','.join(entry.split(',')[0:2])):
        phone_book_dict[','.join(entry.split(',')[0:2])] += f",{','.join(entry.split(',')[2:])}"
    else:
        phone_book_dict.setdefault(','.join(entry.split(',')[0:2]), ','.join(entry.split(',')[2:]))

phone_book_sort = []
for key, value in phone_book_dict.items():
    phone_book_sort.append(list(key.split(',')) + list(value.split(',')))

phone_book_final = []
for entry in phone_book_sort:
    entry = list(dict().fromkeys(entry))
    for item in entry:
        if item[0] == '+':
            if item.count('доб'):
                entry.append(entry.pop(entry.index(item)))
            else:
                if item.count(' '):
                    entry.append(entry.pop(entry.index(item)).replace(' ', ''))
    for item in entry:
        if item.count('@'):
            entry.append(entry.pop(entry.index(item)))
    phone_book_final.append(entry)

# Код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf8") as file:
    datawriter = csv.writer(file, delimiter=',')
    datawriter.writerows(phone_book_final)
