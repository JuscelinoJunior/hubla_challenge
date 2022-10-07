from flask import Flask, jsonify, request
from sqlalchemy.orm import Session

from persistency import db_engine
from persistency.models.sale_model import Sale
from persistency.sales_persistency import retrieve_sales

app = Flask(__name__)

error_message = {"Error": "Internal Error"}


@app.route("/upload_sales", methods=["POST"])
def upload_file():
    request_data = request.files.to_dict()

    data = request_data["file"].read().decode("ascii")

    sale_models = []

    for line in data.splitlines():
        sale_model = Sale()
        sale_model.type = line[0]
        sale_model.product = line[26:55]
        sale_model.value = line[56:65]
        sale_model.seller = line[66:85]
        sale_models.append(sale_model)

    db_session = Session(db_engine)

    try:
        db_session.bulk_save_objects(sale_models)
        db_session.commit()
    except Exception as error:
        db_session.rollback()
        print(error)
    finally:
        db_session.close()

    return jsonify({"file": data})


@app.route("/sales", methods=["GET"])
def read_sales():
    db_session = Session(db_engine)

    sale_models = retrieve_sales(db_session)

    sales_response = []
    for sale in sale_models:
        sale_dict = {
            "id": sale.id,
            "type": sale.type,
            "seller": sale.seller,
            "product": sale.product,
            "value": sale.value,
        }
        sales_response.append(sale_dict)

    return jsonify(sales_response)


if __name__ == "__main__":
    app.run(debug=True)
