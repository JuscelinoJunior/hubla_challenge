from typing import List

from requests import Session

from persistency.models.sale_model import Sale


def retrieve_sales(db_session: Session) -> List[Sale]:
    return db_session.query(Sale)
