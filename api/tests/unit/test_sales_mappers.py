import os

from flask import Request

from mappers.sales_mappers import (
    map_sale_models_list_to_upload_file_response,
    map_retrieved_sales_to_response,
    map_upload_file_request_to_model_list,
)
from persistency.models.sale_model import Sale
from persistency.models.sale_type_model import SaleType
from tests.conftest import create_sales_file
from utils.sales_utils import convert_date_text_to_datetime


def test_map_sale_models_list_to_upload_file_response():
    expected_dict_one = {
        "id": 1,
        "type": 1,
        "date": convert_date_text_to_datetime("2022-01-15T19:20:30-03"),
        "product": "CURSO DE BEM-ESTAR",
        "value": 12.75,
        "seller": "JOSE CARLOS",
    }

    expected_dict_two = {
        "id": 2,
        "type": 2,
        "date": convert_date_text_to_datetime("2022-01-15T19:20:30-03"),
        "product": "CURSO DE BEM-ESTAR",
        "value": 12.75,
        "seller": "JOSE CARLOS",
    }

    sale_model_one = Sale(
        id=expected_dict_one["id"],
        type=expected_dict_one["type"],
        date=expected_dict_one["date"],
        product=expected_dict_one["product"],
        value=expected_dict_one["value"],
        seller=expected_dict_one["seller"],
    )

    sale_model_two = Sale(
        id=expected_dict_two["id"],
        type=expected_dict_two["type"],
        date=expected_dict_two["date"],
        product=expected_dict_two["product"],
        value=expected_dict_two["value"],
        seller=expected_dict_two["seller"],
    )

    sale_models = [sale_model_one, sale_model_two]

    mapped_dict = map_sale_models_list_to_upload_file_response(sale_models)

    assert mapped_dict[0] == expected_dict_one
    assert mapped_dict[1] == expected_dict_two


def test_map_retrieved_sales_to_response():
    expected_dict_one = {
        "id": 1,
        "type": "Venda produtor",
        "date": convert_date_text_to_datetime("2022-01-15T19:20:30-03"),
        "product": "CURSO DE BEM-ESTAR",
        "value": 12.75,
        "seller": "JOSE CARLOS",
    }

    expected_dict_two = {
        "id": 2,
        "type": "Venda produtor",
        "date": convert_date_text_to_datetime("2022-01-15T19:20:30-03"),
        "product": "CURSO DE BEM-ESTAR",
        "value": 12.75,
        "seller": "JOSE CARLOS",
    }

    sale_type_model = SaleType(description="Venda produtor")

    sale_model_one = Sale(
        id=expected_dict_one["id"],
        sale_type=sale_type_model,
        date=expected_dict_one["date"],
        product=expected_dict_one["product"],
        value=expected_dict_one["value"],
        seller=expected_dict_one["seller"],
    )

    sale_model_two = Sale(
        id=expected_dict_two["id"],
        sale_type=sale_type_model,
        date=expected_dict_two["date"],
        product=expected_dict_two["product"],
        value=expected_dict_two["value"],
        seller=expected_dict_two["seller"],
    )

    sale_models = [sale_model_one, sale_model_two]

    mapped_dict = map_retrieved_sales_to_response(sale_models)

    assert mapped_dict[0] == expected_dict_one
    assert mapped_dict[1] == expected_dict_two


def test_map_upload_file_request_to_model_list(create_sales_file):
    try:
        # Create a new txt file and write sales to use to request
        file_parameters = {"file": open(create_sales_file, "rb")}

        # Create a flask request instance with the file example to use as parameter
        request = Request(environ={})
        request.__dict__ = {"files": file_parameters}

        sale_models = map_upload_file_request_to_model_list(request)

        assert sale_models[0].value == 127.5
    finally:
        if os.path.exists(create_sales_file):
            os.remove(create_sales_file)
