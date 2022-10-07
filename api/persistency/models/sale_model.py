from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, and_
from sqlalchemy.orm import relationship, backref

from persistency import Base
from persistency.models.sale_type_model import SaleType


class Sale(Base):
    __tablename__ = "sale"
    __friendly_class_name__ = "Sale"

    id = Column("sale_id", Integer, primary_key=True, nullable=False)
    type = Column(Integer, ForeignKey(SaleType.id), nullable=False)
    date = Column(DateTime)
    product = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)
    seller = Column(Text, nullable=False)

    sale_type = relationship(
        SaleType,
        foreign_keys=[type],
        primaryjoin=and_(SaleType.id == type),
        lazy="joined",
        backref=backref("sale_type", lazy="noload"),
    )
