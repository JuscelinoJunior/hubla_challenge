from sqlalchemy import Column, Integer, Text

from persistency import Base


class SaleType(Base):
    __tablename__ = "sale_type"
    __friendly_class_name__ = "Sale Type"

    id = Column("sale_type_id", Integer, primary_key=True, nullable=False)
    description = Column(Text, nullable=False)
    kind = Column(Text, nullable=False)
    signal = Column(Text, nullable=False)
