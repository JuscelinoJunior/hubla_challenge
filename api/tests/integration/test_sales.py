import os

from tests.request_utils import request_to_api


def test_upload_file_with_sales(create_sales_file):
    try:
        # Create a new txt file and write sales to use to request
        file_parameters = {"file": open(create_sales_file, "rb")}

        upload_sales_response, status_code = request_to_api(
            endpoint="/upload_sales", file=file_parameters, method="POST"
        )

        assert status_code == 201
        assert upload_sales_response[0]["product"] == "CURSO DE BEM-ESTAR"
    finally:
        if os.path.exists(create_sales_file):
            os.remove(create_sales_file)


def test_get_sales():
    sales_response, status_code = request_to_api(
        endpoint="/sales", file=None, method="GET"
    )

    assert status_code == 200
    assert isinstance(sales_response, list)
