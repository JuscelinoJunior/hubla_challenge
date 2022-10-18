from typing import Dict, Any, List, Tuple

import connexion
from flask import jsonify, request, Response
from flask_cors import CORS
from sqlalchemy.orm import Session

from mappers.sales_mappers import (
    map_upload_file_request_to_model_list,
    map_sale_models_list_to_upload_file_response,
    map_retrieved_sales_to_response,
)
from persistency import db_engine
from persistency.models.sale_model import Sale
from persistency.sales_persistency import retrieve_sales


def upload_sales() -> Tuple[Response, int]:
    """
    Upload a txt file with sales and save it on the database.

    :return: Response
    """
    sale_models: List[Sale] = map_upload_file_request_to_model_list(request)

    db_session: Session = Session(db_engine)

    try:
        db_session.bulk_save_objects(sale_models, return_defaults=True)
        db_session.commit()

        upload_file_response: List[
            Dict[str, Any]
        ] = map_sale_models_list_to_upload_file_response(sale_models)
        return jsonify(upload_file_response), 201
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()


def read_sales() -> Response:
    """
    Retrieve a list with all sales registered on the database.

    :return: Response
    """
    db_session = Session(db_engine)

    try:
        sale_models: List[Sale] = retrieve_sales(db_session)
        sales_response: List[Dict[str, Any]] = map_retrieved_sales_to_response(
            sale_models
        )
    except Exception as exception:
        db_session.rollback()
        raise exception

    return jsonify(sales_response)


if __name__ == "__main__":
    app = connexion.FlaskApp(__name__, specification_dir="openapi_specifications/")
    flask_app = app.app
    CORS(flask_app)
    app.add_api("api.json")
    app.run(debug=True)
