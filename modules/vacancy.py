from typing import List

from modules.salary import Salary
from modules.string_handler import StringHandler


class Vacancy:
    """Класс для представления вакансии"""

    def __init__(self, row: List[str], title: List[str]):
        """
        Инициализирует объект класса Vacancy
        :param row: Строка с вакансией из csv файла
        :param title: Названия столбцов csv файла
        """
        self.__name = None
        self.__salary = None
        self.__area_name = None
        self.__published_at = None
        self.__salary_from = None
        self.__salary_to = None
        self.__salary_currency = None

        fields_cases = {
            'name': lambda value: self.__set_value('name', StringHandler.delete_rubbish(value)),
            'salary_from': lambda value: self.__set_value('salary_from', StringHandler.delete_rubbish(value)),
            'salary_to': lambda value: self.__set_value('salary_to', StringHandler.delete_rubbish(value)),
            'salary_currency': lambda value: self.__set_value('salary_currency', StringHandler.delete_rubbish(value)),
        }

        for i, field in enumerate(row):
            if title[i] not in fields_cases:
                continue

            fields_cases[title[i]](field)

        self.__set_salary()

    def get_salary(self) -> float:
        """Возращает зарплату в рублях для данной вакансии"""
        return float(self.__salary)

    def is_suitible(self, name: str) -> bool:
        """
        Содержит ли в названии name
        :param name: Название вакансии
        """
        return self.__name.count(name) > 0

    def __set_value(self, key, value):
        """
        Метод для инициализации приватных полей объекта
        :param key: Название поля
        :param value: Значение поля
        """
        self.__dict__['_Vacancy__' + key] = value

    def __set_salary(self):
        """Инициализирует зарплату при инициализации объекта"""
        self.__salary = Salary(self.__salary_from, self.__salary_to, self.__salary_currency)