import csv
import re


class Phonebook:
    def __init__(self):
        self.contacts_list = None
        self.new_contact = []


# выгрузка из файла
    def get_list(self) -> list:
        with open("phonebook_raw.csv") as f:
            rows = csv.reader(f, delimiter=",")
            self.contacts_list = list(rows)
            return self.contacts_list


 # запись нового csv
    def record(self):
        with open("phonebook.csv", "w") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(self.new_contact)


# Корректируем ФИО
    def correct_name(self, item: list):
        pattern = re.compile("^(\w+)([\s,]\w+)?([\s,]\w+)")
        text = " ".join(item)
        result = pattern.search(text)
        item[:2] = result.group(0).split()
        return item

# Поиск по совпадению ФИ
    def chek_name(self, item: list):
        for items in self.new_contact:
            if item[0] == items[0] and item[1] == items[1]:
                for i, _ in enumerate(items):
                    if len(str(_)) <= 1:
                        items[i] = item[i]
                return
        else:
            self.new_contact.append(item)
            return


# Корректируем номер
    def correct_phone(self, item: list):
        pattern = re.compile(r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*"
                             r"(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*")
        subst_pattern = r"+7(\2)\3-\4-\5 \6\7"
        result = pattern.sub(subst_pattern, item[6])
        item[6] = result
        return item


    def get_correction(self):
        self.new_contact.append(self.contacts_list[0])
        for item in self.contacts_list[1:]:
            self.correct_name(item)
            self.correct_phone(item)
            self.chek_name(item)
