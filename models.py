from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    barcode = Column(String, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.id"))

    donor = relationship("Donor", back_populates="items")



class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    weighs = Column(Boolean, nullable=False, default=False)

    items = relationship("Item", back_populates="donor")
    weights = relationship("DonorWeight", back_populates="donor")



class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    passhash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False)

    transactions = relationship("Transaction", back_populates="manager")



class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    time = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.id"))

    manager = relationship("Manager", back_populates="transactions")
    items = relationship("TransactionItem", back_populates="transaction")
    weights = relationship("DonorWeight", back_populates="transaction")



class TransactionItem(Base):
    __tablename__ = "transaction_items"

    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    item = relationship("Item")
    transaction = relationship("Transaction", back_populates="items")



class DonorWeight(Base):
    __tablename__ = "donor_weights"
    
    donor_id = Column(Integer, ForeignKey("donors.id"), primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)
    weight = Column(Float, nullable=False, default=0.0)

    transaction = relationship("Transaction", back_populates="weights")
    donor = relationship("Donor", back_populates="weights")
    