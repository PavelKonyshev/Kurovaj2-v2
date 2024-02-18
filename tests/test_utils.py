from pathlib import Path
import pytest
from src import utils

CURRENT_PATH = Path(__file__).parent
PATH_WITH_FIXTURE = Path.joinpath(CURRENT_PATH, 'src', 'operations.json')


@pytest.fixture
def bank_fixture():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на счет",
            "from": "Maestro 3928549031574026",
            "to": "Счет 84163357546688983493"
        },
        {}
    ]


@pytest.fixture
def bank_fixture_2():
    return "Maestro 1596837868705199"


@pytest.fixture
def bank_fixture_3():
    return "Счет 84163357546688983493"


@pytest.fixture
def bank_fixture_4():
    return "Unknown"


@pytest.fixture
def bank_fixture_5():
    return "2019-08-26"


@pytest.fixture
def bank_fixture_6():
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }


@pytest.fixture
def bank_fixture_7():
    return [{
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-12-08T10:50:58.294041",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 64686473678894775907"
    }
    ]


def test_last_operations(bank_fixture):
    assert len(utils.last_operations(bank_fixture)) == 5


def test_mask_card_number(bank_fixture_2, bank_fixture_3, bank_fixture_4):
    assert utils.mask_card_number(bank_fixture_2) == "Maestro 1596 83** **** 5199"
    assert utils.mask_card_number(bank_fixture_3) == "Счет **3493"
    assert utils.mask_card_number(bank_fixture_4) == "Unknown"


def test_mask_account_number(bank_fixture_3):
    assert utils.mask_account_number(bank_fixture_3) == "Счет **3493"


def test_format_date(bank_fixture_5):
    assert utils.format_date(bank_fixture_5) == '26.08.2019'


def test_format_operation(bank_fixture_6):
    formatted_operation = utils.format_operation(bank_fixture_6)
    assert formatted_operation == '26.08.2019 Перевод организации\n' \
                                  'Maestro 1596 83** **** 5199 -> Счет **9589\n' \
                                  '31957.58 руб.\n'


def test_print_last_operations(bank_fixture_7):
    assert utils.print_last_operations(bank_fixture_7) == ['08.12.2019 Открытие вклада\n'
                                                           'Unknown -> Счет **5907\n'
                                                           '41096.24 USD\n']