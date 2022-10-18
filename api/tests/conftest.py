import uuid

import pytest


@pytest.fixture
def create_sales_file():
    def _method(text=None):
        file_name = str(uuid.uuid4()) + "test_file.txt"

        if text is None:
            text = (
                "12022-01-15T19:20:30-03:00CURSO DE BEM-ESTAR            0000012750JOSE CARLOS\n"
                + "12021-12-03T11:46:02-03:00DOMINANDO INVESTIMENTOS       0000050000MARIA CANDIDA\n"
                + "22022-01-16T14:13:54-03:00CURSO DE BEM-ESTAR            0000012750THIAGO OLIVEIRA"
            )

        with open(file_name, "w") as f:
            f.write(text)

        return file_name

    return _method
