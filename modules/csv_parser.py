import csv
import math
import os
import time
from multiprocessing import Pool
from typing import Dict, List, Tuple
import concurrent.futures as pool

from modules.vacancy import Vacancy


def profile(func):
    """
    Функция для профилирования
    :param func: Функция
    :return: Результат выполнения функции
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Time: %.03f s" % (end - start))
        return result

    return wrapper


class CsvParser:
    """
    Класс для представления сущности парсера
    """
    def __init__(self):
        """
        Инициализация парсера
        """
        self.__year_data: Dict[str, List[List[str]]] = {}
        self.__title = []

    def create_years_csv(self, file_name: str, output_dir: str):
        """
        Метод создает csv файлы, разделенные по годам
        :param file_name: Название файла для парсинга
        :param output_dir: Название директории для чанков
        :return:
        """
        self.__parse_csv(file_name)
        self.__write_csv(output_dir)

    @staticmethod
    @profile
    def get_statictics(dir_csv: str, filter_name: str) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int], Dict[str, int]]:
        """
        Функция для получения данных о вакансиях для печати
        :param dir_csv: Название деректиории с чанками
        :param filter_name: Название вакансии для выборки
        :return: Кортеж из словарей данных для печати
        """
        salaries = {}
        count = {}
        salaries_filtered = {}
        count_filtered = {}

        files = os.listdir(dir_csv)
        args = list(map(lambda x: (dir_csv, x, filter_name), files))

        mult_pool = Pool(len(files))

        for e in sorted(mult_pool.starmap(get__year_statistics, args), key=lambda x: x[0]):
            salaries[e[0]] = e[1]
            count[e[0]] = e[2]
            salaries_filtered[e[0]] = e[3]
            count_filtered[e[0]] = e[4]

        return salaries, count, salaries_filtered, count_filtered

    # @staticmethod
    # @profile
    # def get_statictics(dir_csv: str, filter_name: str) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int], Dict[str, int]]:
    #     """
    #     Функция для получения данных о вакансиях для печати
    #     :param dir_csv: Название деректиории с чанками
    #     :param filter_name: Название вакансии для выборки
    #     :return: Кортеж из словарей данных для печати
    #     """
    #     salaries = {}
    #     count = {}
    #     salaries_filtered = {}
    #     count_filtered = {}
    #
    #     files = os.listdir(dir_csv)
    #     args = list(map(lambda x: (dir_csv, x, filter_name), files))
    #
    #     with pool.ProcessPoolExecutor(max_workers=len(files)) as executer:
    #         wait_complete = []
    #
    #         for arg in args:
    #             future = executer.submit(get__year_statistics, *arg)
    #             wait_complete.append(future)
    #
    #     result = sorted((map(lambda x: x.result(), pool.as_completed(wait_complete))), key=lambda x: x[0])
    #
    #     for arg in result:
    #         salaries[arg[0]] = arg[1]
    #         count[arg[0]] = arg[2]
    #         salaries_filtered[arg[0]] = arg[3]
    #         count_filtered[arg[0]] = arg[4]
    #
    #     return salaries, count, salaries_filtered, count_filtered

    def __parse_csv(self, file_name: str):
        """
        Метод для парсинга файла
        :param file_name: Название файла для парсинга
        :return:
        """
        with open(file_name, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=',')

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

    def __write_csv(self, output_dir: str):
        """
        Метод записывает данные в отдельные csv файлы по годам в папке output_dir
        :param output_dir: Название директории для чанков
        :return:
        """
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        for key in self.__year_data.keys():
            with open(f"{output_dir}/{key}.csv", 'w', encoding='utf-8-sig') as f:
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


def get__year_statistics(dir_csv: str, file_name: str, filter_name: str) -> Tuple[str, int, int, int, int]:
    """
    Функция для получения статистики по годам

    :param dir_csv: Название деректиории с чанками
    :param file_name: Название чанка для обработки
    :param filter_name: Название вакансии для выборки
    :return: Кортеж со статистикой для чанка
    """
    vacancies_count = 0
    vacancies_sum = 0
    vacancies_filtered_count = 0
    vacancies_filtered_sum = 0
    title = []

    with open(f"{dir_csv}/{file_name}", 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',')

        is_title = True

        for row in reader:
            if is_title:
                title = row
                is_title = False
                continue

            vacancy = Vacancy(row, title)

            vacancies_count += 1
            salary = vacancy.get_salary()
            vacancies_sum += salary

            if vacancy.is_suitible(filter_name):
                vacancies_filtered_count += 1
                vacancies_filtered_sum += salary

    result = (
        file_name[0:4],
        math.floor(vacancies_sum / vacancies_count) if vacancies_count > 0 else 0,
        vacancies_count,
        math.floor(vacancies_filtered_sum / vacancies_filtered_count) if vacancies_filtered_count > 0 else 0,
        vacancies_filtered_count,
    )

    return result