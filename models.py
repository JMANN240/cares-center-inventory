from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Donor(Base):
    __tablename__ = "donors"

    donor_id = Column(Integer, primary_key=True)
    donor_name = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="donor")

class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    item_points = Column(Integer, nullable=False)
    item_front_quantity = Column(Integer, nullable=False, default=0)
    item_back_quantity = Column(Integer, nullable=False, default=0)
    item_barcode = Column(String, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.donor_id"))

    donor = relationship("Donor", back_populates="items")