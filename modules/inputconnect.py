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

    def read_console(self):
        """
        Метод для чтения данных из консоли
        :return:
        """
        self.file_name = input('Введите название файла: ')
        self.output_dir = input('Введите название директории для чанков: ')