from typing import Dict, Tuple


class InputConnect:
    """
    Метод для предоставления связи с пользователем

    Attributes:
        file_name (str): Название файла для парсинга
    """
    def __init__(self):
        """
        Метод инициализации объекта класса InputConnect
        """
        self.file_name: str = ''
        self.output_dir: str = ''
        self.filter_name: str = ''

    def read_console(self):
        """
        Метод для чтения данных из консоли
        :return:
        """
        self.file_name = input('Введите название файла: ')
        self.output_dir = input('Введите название директории для чанков: ')
        self.filter_name = input('Введите название профессии: ')

    def write_console(self, data: Tuple[Dict[str, int], Dict[str, int], Dict[str, int], Dict[str, int]]):
        print(f"Динамика уровня зарплат по годам: {data[0]}")
        print(f"Динамика количества вакансий по годам: {data[1]}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {data[2]}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {data[3]}")