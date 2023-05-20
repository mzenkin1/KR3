from datetime import datetime
import json
from config import SOURCE_PATH


def get_data():

    """Получаем данные из файла"""

    try:
        with open(SOURCE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Файл не найден")
    except json.JSONDecodeError:
        print("Файл не удается преобразовать")


def get_filtered_data(data, filter_empty_from=False):

    """Фильтруем операции по EXECUTED"""

    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]
    if filter_empty_from:
        data = [x for x in data if "from" in x]
    return data


def get_last_values(data, count_last_values):

    """Сортируем список в обратном порядке по дате"""

    data = sorted(data, key=lambda x: x["date"], reverse=True)
    data = data[:count_last_values]
    return data


def get_formatted_data(data):

    """Выполняем форматирование значений"""

    formatted_data = []
    for row in data:
        date = datetime.strptime(row["date"],
                                 "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = row["description"]
        recipient = f"{row['to'].split()[0]} **{row['to'][-4:]}"
        operations_amount = f"{row['operationAmount']['amount']} " \
                            f"{row['operationAmount']['currency']['name']}"
        if "from" in row:
            sender = row["from"].split()
            from_bill = sender.pop(-1)
            from_bill = f"{from_bill[:4]}" \
                        f"{from_bill[4:6]}** *** {from_bill[-4:]}"
            from_info = " ".join(sender)
        else:
            from_info, from_bill = "", ""
        formatted_data.append(f"""\
{date} {description}
{from_info} {from_bill} -> {recipient}
{operations_amount}""")
    return formatted_data
