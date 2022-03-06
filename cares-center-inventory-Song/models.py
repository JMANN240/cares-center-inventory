from sqlalchemy import Column, ForeignKey, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Donor(Base):
    __tablename__ = "donors"

    donor_id = Column(Integer, primary_key=True)
    donor_name = Column(String, unique=True, nullable=False)

    to_items = relationship("Item", back_populates="to_donors")
    to_donor_weight = relationship("DonorWeight", back_populates="to_donors")

class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    item_points = Column(Integer, CheckConstraint("item_points < 30"), nullable=False)
    item_front_quantity = Column(Integer, nullable=False, default=0)
    #item_back_quantity = Column(Integer, nullable=False, default=0)
    item_barcode = Column(String, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.donor_id"))

    to_donors = relationship("Donor", back_populates="to_items")
    to_replenish_items = relationship("ReplenishItem", back_populates="to_items")
    to_transaction_items = relationship("TransactionItem", back_populates="to_items")

class Manager(Base):
    __tablename__ = "managers"

    manager_id = Column(Integer, primary_key=True)
    manager_name = Column(String, unique=True, nullable=False)
    passcode = Column(String, nullable=False)

    to_replenish_history = relationship("ReplenishHistory", back_populates="to_managers")
    to_transaction_history = relationship("TransactionHistory", back_populates="to_managers")

class ReplenishHistory(Base):
    __tablename__ = "replenish_history"

    replenish_id = Column(Integer, primary_key=True)
    replenish_date = Column(String, nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.manager_id"))

    to_managers = relationship("Manager", back_populates="to_replenish_history")
    to_replenish_items = relationship("ReplenishItem", back_populates="to_replenish_history")

class ReplenishItem(Base):
    __tablename__ = "replenish_items"

    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    replenish_id = Column(Integer, ForeignKey("replenish_history.replenish_id"), primary_key=True)
    replenish_quantity = Column(Integer, nullable=False)

    to_items = relationship("Item", back_populates="to_replenish_items")
    to_replenish_history = relationship("ReplenishHistory", back_populates="to_replenish_items")

class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    transaction_id = Column(Integer, primary_key=True)
    transaction_date = Column(String, nullable=False)
    transaction_points = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.manager_id"))

    to_managers = relationship("Manager", back_populates="to_transaction_history")
    to_transaction_items = relationship("TransactionItem", back_populates="to_transaction_history")
    to_donor_weight = relationship("DonorWeight", back_populates="to_transaction_history")

class TransactionItem(Base):
    __tablename__ = "transaction_items"

    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction_history.transaction_id"), primary_key=True)
    transaction_quantity = Column(Integer, nullable=False)

    to_items = relationship("Item", back_populates="to_transaction_items")
    to_transaction_history = relationship("TransactionHistory", back_populates="to_transaction_items")

class DonorWeight(Base):
    __tablename__ = "donor_weight"
    
    donor_id = Column(Integer, ForeignKey("donors.donor_id"), primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction_history.transaction_id"), primary_key=True)
    weight = Column(Float, nullable=False, default=0.0)

    to_transaction_history = relationship("TransactionHistory", back_populates="to_donor_weight")
    to_donors = relationship("Donor", back_populates="to_donor_weight")