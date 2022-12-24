import re


class StringHandler:
    """
    Класс, содержащий в себе вспомогатильные функции которые могут быть переиспользованы
    """

    @staticmethod
    def delete_rubbish(s: str) -> str:
        """
        Удаляет html теги и лишние пробелы из строки
        :param s: Строка для чистки
        :return: Очищенная строка
        """
        rubbish_html = re.compile('<.*?>')

        return ' '.join(re.sub(rubbish_html, '', s).split()).strip()

    @staticmethod
    def refactor_label(label: str) -> str:
        """
        Форматирование подписи круговой даиграммы
        :param label: Подпись
        :return: Отформатированная подпись
        """
        spaces = re.compile('\s+')
        line = re.compile('-+')

        label = re.sub(spaces, '\n', label)
        return re.sub(line, '-\n', label)