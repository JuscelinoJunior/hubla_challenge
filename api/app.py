from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.orm import Session, declarative_base

# SQAlchemy model classes
Base = declarative_base()


class SaleType(Base):
    __tablename__ = "sale_type"
    __friendly_class_name__ = "Sale Type"

    id = Column("sale_type_id", Integer, primary_key=True, nullable=False)
    description = Column(Text, nullable=False)
    kind = Column(Text, nullable=False)
    signal = Column(Text, nullable=False)


class Sale(Base):
    __tablename__ = "sale"
    __friendly_class_name__ = "Sale"

    id = Column("sale_id", Integer, primary_key=True, nullable=False)
    type = Column(Integer, ForeignKey(SaleType.id), nullable=False)
    date = Column(DateTime)
    product = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)
    seller = Column(Text, nullable=False)


# Database connection
db_engine = create_engine("mysql+mysqlconnector://root:root@localhost/hubla_sales")

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
    except Exception as e:
        db_session.rollback()
        print(e)
    finally:
        db_session.close()

    return jsonify({"file": data})


@app.route("/sales", methods=["GET"])
def read_sales():
    db_session = Session(db_engine)

    sale_models = db_session.query(Sale)

    sales_response = []
    for sale in sale_models:
        sale_dict = {"id": sale.id, "type": sale.type, "seller": sale.seller, "product": sale.product, "value": sale.value}
        sales_response.append(sale_dict)

    return jsonify(sales_response)


if __name__ == "__main__":
    app.run(debug=True)
