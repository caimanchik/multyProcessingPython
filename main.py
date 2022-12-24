from modules.csv_parser import CsvParser
from modules.inputconnect import InputConnect


def main():
    """
    Функция для запуска программы
    :return:
    """
    connect = InputConnect()
    connect.read_console()

    parser = CsvParser(connect.file_name)
    parser.create_years_csv()

if __name__ == '__main__':
    main()