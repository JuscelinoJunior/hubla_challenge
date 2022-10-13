from typing import List, Dict, Any

from flask import Request

from persistency.models.sale_model import Sale
from utils.sale_utils import (
    convert_date_text_to_datetime,
    remove_final_spaces_in_a_string,
    convert_value_in_cents_to_reals,
)


def map_upload_file_request_to_model_list(request: Request):
    """
    Map a txt file to a list of sale models.

    Read the file from the request. Convert the file to a string and iterate by the lines.
    Each line is converted to a sale model.

    :param request: The Flask request object
    :type request: Request

    :return: A list of sale models
    """
    request_data: Dict[str, Any] = request.files.to_dict()

    file_data: str = request_data["file"].read().decode("ascii")

    sale_models: List[Sale] = []

    for line in file_data.splitlines():
        sale_model: Sale = Sale(
            type=line[0],
            date=convert_date_text_to_datetime(line[1:25]),
            product=remove_final_spaces_in_a_string(line[26:55]),
            value=convert_value_in_cents_to_reals(int(line[56:65])),
            seller=line[66:85],
        )
        sale_models.append(sale_model)

    return sale_models


def map_sale_models_list_to_upload_file_response(sale_models) -> List[Dict[str, Any]]:
    """
    Map a list of models to a list of dict to be used to the JSON response.

    :param sale_models: a list with all sale models registered on the database
    :type sale_models: List

    :return: a list of dict to be used to the JSON response
    :rtype: List
    """
    upload_file_response: List[Dict[str, Any]] = []

    for sale in sale_models:
        sale_dict = {
            "id": sale.id,
            "type": int(sale.type),
            "date": sale.date,
            "seller": sale.seller,
            "product": sale.product,
            "value": sale.value,
        }
        upload_file_response.append(sale_dict)
    return upload_file_response


def map_retrieved_sales_to_response(sale_models: List[Sale]) -> List[Dict[str, Any]]:
    """
    Map a list of models retrieved from the database to a list of dict to be used to the JSON response.

    :param sale_models: a list with all sale models retrieved from the database
    :type sale_models: List

    :return: a list of dict to be used to the JSON response
    :rtype: List
    """

    retrieve_sales_response: List[Dict[str, Any]] = []

    for sale in sale_models:
        sale_dict: Dict[str, Any] = {
            "id": sale.id,
            "type": sale.sale_type.description,
            "date": sale.date,
            "seller": sale.seller,
            "product": sale.product,
            "value": sale.value,
        }
        retrieve_sales_response.append(sale_dict)
    return retrieve_sales_response
