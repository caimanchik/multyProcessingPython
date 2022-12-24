import csv
import os
from typing import Dict, List


class CsvParser:
    """
    Класс для представления сущности парсера
    """

    def __init__(self, file_name: str):
        """
        Инициализация парсера
        :param file_name: Название файла для парсинга
        """
        self.__file_name = file_name
        self.__year_data: Dict[str, List[List[str]]] = {}
        self.__title = []

    def create_years_csv(self):
        """
        Метод создает csv файлы, разделенные по годам
        :return:
        """
        self.__parse_csv()
        self.__write_csv()

    def __parse_csv(self):
        """
        Метод для парсинга файла
        :return:
        """
        with open('src/' + self.__file_name, 'r', encoding='utf-8-sig') as data_src:
            reader = csv.reader(data_src, delimiter=',')

            is_title = True

            for row in reader:
                if is_title:
                    self.__parse_row(row, True)
                    is_title = False
                    continue

                self.__parse_row(row, False)

    def __parse_row(self, row: List[str], is_title: bool):
        """
        Метод парсит вакансии и добавляет данные по годам в словарь self.__year_data
        :param row: Массив из строки файла
        :param is_title: Является ли строка заголовком
        :return:
        """
        if is_title:
            self.__title = row
            return

        if row.count('') != 0 or len(row) < len(self.__title) - 1: return

        now_year = CsvParser.__get_year_from_row(row)

        year_vacancies = self.__year_data.get(now_year, [])
        year_vacancies.append(row)
        self.__year_data[now_year] = year_vacancies

    def __write_csv(self):
        """
        Метод записывает данные в отдельные csv файлы по годам в папке years_csv
        :return:
        """
        if not os.path.isdir("years_csv"):
            os.mkdir("years_csv")

        for key in self.__year_data.keys():
            with open('years_csv/' + key + '.csv', 'w', encoding='utf-8-sig') as f:
                writer = csv.writer(f)

                writer.writerow(self.__title)
                writer.writerows(self.__year_data[key])

    @staticmethod
    def __get_year_from_row(row: List[str]) -> str:
        """
        Возвращает год вакансии из строки csv файла
        :param row: Массив из строки
        :return: Дата
        """
        return row[-1][0:4]