import json
from datetime import datetime


def operations_file(filename):
    """
    Возвращает файл json с
    данными по банковским операциям.
    """
    with open(filename, encoding='utf-8') as file:
        operations = json.load(file)
        return operations


def last_operations(operations):
    """
    Выбирает выполненные операции, сортирует
    их по дате и возвращает список 5-ти последних операций.
    """
    ex_operations = [op for op in operations if op.get('state') == 'EXECUTED']
    sorted_operations = sorted(ex_operations, key=lambda operation: operation['date'], reverse=True)
    five_last_operations = sorted_operations[:5]
    return five_last_operations


def mask_card_number(card_number):
    """
    Возвращает замаскированные номера счетов
    и карт отправителя если они есть.
    """
    if 'Счет' in card_number:
        masked_number = card_number[:5] + '**' + card_number[-4:]
        return masked_number
    elif 'Unknown' in card_number:
        return 'Unknown'
    else:
        masked_number = card_number[:-16] + card_number[-16:-12] + ' ' + \
                        card_number[-12:-10] + '** **** ' + card_number[-4:]
        return masked_number


def mask_account_number(account_number):
    """Возвращает замаскированные номера счетов получателя."""
    masked_number = account_number[:5] + '**' + account_number[-4:]
    return masked_number


def format_date(date_str):
    """
    Возврашает отформатированную дату вида ДД.ММ.ГГГГ.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")


def format_operation(operation):
    """
    Отформатированные данные для
    вывода информации пользователю.
    """
    # Дата банковской операции.
    date = format_date(operation['date'][:10])

    # Описание банковской операции.
    description = operation['description']

    # Номер "от" кого перевод (если он виден) и
    # номер "кому" перевод
    from_card = operation.get('from', 'Unknown')
    to_card = operation['to']

    # Сумма и валюта перевода.
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    # Вызов функций маскирующих номера счетов/карт.
    masked_from = mask_card_number(from_card)
    masked_to = mask_account_number(to_card)

    return f'{date} {description}\n{masked_from} -> {masked_to}\n{amount} {currency}\n'


def print_last_operations(five_last_operations):
    """
    Выводит пользователю 5 последних
    операций в определенном формате.
    """
    form_operation = [format_operation(operation) for operation in five_last_operations]
    return form_operation