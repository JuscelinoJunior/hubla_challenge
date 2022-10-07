from persistency.models.sale_model import Sale


def retrieve_sales(db_session):
    return db_session.query(Sale)
