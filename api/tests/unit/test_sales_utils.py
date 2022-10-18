from datetime import datetime

from utils.sales_utils import (
    convert_value_in_cents_to_reals,
    remove_final_spaces_in_a_string,
    convert_date_text_to_datetime,
)


def test_convert_value_in_cents_to_reals():
    converted_value = convert_value_in_cents_to_reals(12750)

    assert converted_value == 127.5


def test_remove_final_spaces_in_a_string():
    converted_string = remove_final_spaces_in_a_string("ABC           ")

    assert converted_string == "ABC"


def test_convert_date_text_to_datetime():
    converted_date_time = convert_date_text_to_datetime("2022-01-15T19:20:30-03:00")

    assert isinstance(converted_date_time, datetime)
    assert converted_date_time.day == 15
    assert converted_date_time.month == 1
    assert converted_date_time.year == 2022
    assert converted_date_time.hour == 19
    assert converted_date_time.minute == 20
    assert converted_date_time.second == 30
