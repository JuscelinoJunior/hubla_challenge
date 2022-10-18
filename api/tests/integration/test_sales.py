import os

from tests.request_utils import request_to_api


def test_upload_file_with_sales(create_sales_file):
    sales_file = create_sales_file()
    try:
        # Create a new txt file and write sales to use to request
        file_parameters = {"file": open(sales_file, "rb")}

        upload_sales_response, status_code = request_to_api(
            endpoint="/upload_sales", file=file_parameters, method="POST"
        )

        assert status_code == 201
        assert upload_sales_response[0]["product"] == "CURSO DE BEM-ESTAR"
    finally:
        if os.path.exists(sales_file):
            os.remove(sales_file)


def test_upload_file_with_sales_with_blank_line(create_sales_file):
    file_text_with_blankline = (
            "12022-01-15T19:20:30-03:00CURSO DE BEM-ESTAR            0000012750JOSE CARLOS\n"
            + "\n"
            + "12021-12-03T11:46:02-03:00DOMINANDO INVESTIMENTOS       0000050000MARIA CANDIDA\n"
            + "22022-01-16T14:13:54-03:00CURSO DE BEM-ESTAR            0000012750THIAGO OLIVEIRA"
    )

    sales_file = create_sales_file(file_text_with_blankline)

    try:
        # Create a new txt file and write sales to use to request
        file_parameters = {"file": open(sales_file, "rb")}

        upload_sales_response, status_code = request_to_api(
            endpoint="/upload_sales", file=file_parameters, method="POST"
        )

        assert status_code == 400
        assert (
            "It's not possible to read the sales from your file"
            in upload_sales_response["detail"]
        )
    finally:
        if os.path.exists(sales_file):
            os.remove(sales_file)


def test_upload_file_with_sales_without_type(create_sales_file):
    file_text_without_type = (
            "2022-01-15T19:20:30-03:00CURSO DE BEM-ESTAR            0000012750JOSE CARLOS\n"
            + "12021-12-03T11:46:02-03:00DOMINANDO INVESTIMENTOS       0000050000MARIA CANDIDA\n"
    )

    sales_file = create_sales_file(file_text_without_type)

    try:
        # Create a new txt file and write sales to use to request
        file_parameters = {"file": open(sales_file, "rb")}

        upload_sales_response, status_code = request_to_api(
            endpoint="/upload_sales", file=file_parameters, method="POST"
        )

        assert status_code == 400
        assert (
            "It's not possible to read the sales from your file"
            in upload_sales_response["detail"]
        )
    finally:
        if os.path.exists(sales_file):
            os.remove(sales_file)


def test_get_sales():
    sales_response, status_code = request_to_api(
        endpoint="/sales", file=None, method="GET"
    )

    assert status_code == 200
    assert isinstance(sales_response, dict)
