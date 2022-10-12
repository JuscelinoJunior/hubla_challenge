import datetime
from dateutil.parser import parse


def convert_value_in_cents_to_reals(value: int) -> float:
    return float(value / 100)


def remove_final_spaces_in_a_string(text: str) -> str:
    return text.strip()


def convert_date_text_to_datetime(sale_datetime: str) -> datetime:
    return parse(sale_datetime)
