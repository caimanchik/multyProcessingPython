from modules.csv_parser import CsvParser
from modules.inputconnect import InputConnect


def main():
    """
    Функция для запуска программы
    :return:
    """
    connect = InputConnect()
    connect.read_console()

    parser = CsvParser()
    parser.create_years_csv(connect.file_name, connect.output_dir)

    data = parser.get_statictics(connect.output_dir, connect.filter_name)
    connect.write_console(data)


if __name__ == '__main__':
    main()