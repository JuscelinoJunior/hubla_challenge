from typing import Dict, Any, List

import connexion
from flask import jsonify, request, Request, Response
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


def upload_sales() -> Response:
    sale_models: Request = map_upload_file_request_to_model_list(request)

    db_session: Session = Session(db_engine)

    try:
        db_session.bulk_save_objects(sale_models)
        db_session.commit()

        upload_file_response: List[
            Dict[str, Any]
        ] = map_sale_models_list_to_upload_file_response(sale_models)
        return jsonify(upload_file_response)
    except Exception as exception:
        db_session.rollback()
        print(exception)
        raise exception
    finally:
        db_session.close()


def read_sales() -> Response:
    db_session = Session(db_engine)

    try:
        sale_models: List[Sale] = retrieve_sales(db_session)
        sales_response: List[Dict[str, Any]] = map_retrieved_sales_to_response(
            sale_models
        )
        return jsonify(sales_response)
    except Exception as exception:
        raise exception


if __name__ == "__main__":
    app = connexion.FlaskApp(__name__, specification_dir="openapi_specifications/")
    flask_app = app.app
    CORS(flask_app)
    app.add_api("api.json")
    app.run(debug=True)
