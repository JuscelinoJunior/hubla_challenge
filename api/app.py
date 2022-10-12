import connexion
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.orm import Session

from mappers.sales_mappers import (
    map_upload_file_request_to_model_list,
    map_sale_models_list_to_upload_file_response,
    map_retrieved_sales_to_response,
)
from persistency import db_engine
from persistency.sales_persistency import retrieve_sales

app = Flask(__name__)


def upload_sales():
    sale_models = map_upload_file_request_to_model_list(request)

    db_session = Session(db_engine)

    try:
        db_session.bulk_save_objects(sale_models)
        db_session.commit()
    except Exception as error:
        db_session.rollback()
        print(error)
    finally:
        db_session.close()

    upload_file_response = map_sale_models_list_to_upload_file_response(sale_models)

    return jsonify(upload_file_response)


def read_sales():
    db_session = Session(db_engine)

    sale_models = retrieve_sales(db_session)

    sales_response = map_retrieved_sales_to_response(sale_models)

    return jsonify(sales_response)


if __name__ == "__main__":
    app = connexion.FlaskApp(__name__, specification_dir="openapi_specifications/")
    flask_app = app.app
    CORS(flask_app)
    app.add_api("api.json")
    app.run(debug=True)
