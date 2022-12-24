class Salary:
    """
    Класс для представления зарплаты
    """
    __currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(
            self,
            salary_from: str | float,
            salary_to: str | float,
            salary_currency: str,
    ):
        """
        Инициализирует объект Salary
        Args:
            salary_from (str | float): Нижняя граница оклада
            salary_to (str | float): Верхняя граница оклада,
            salary_currency (str): Валюта оклада
        """
        self.__salary_from, self.__salary_to, self.__salary_currency = salary_from, salary_to, salary_currency

    def __float__(self) -> float:
        """
        Преобразует зарплату к float значению в рублях
        """
        return (float(self.__salary_from) + float(self.__salary_to)) / 2 * self.__currency_to_rub[self.__salary_currency.upper()]
