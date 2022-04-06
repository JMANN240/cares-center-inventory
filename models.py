from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Donor(Base):
    __tablename__ = "donor"

    donor_id = Column(Integer, primary_key=True)
    donor_name = Column(String, unique=True, nullable=False)

    to_item = relationship("Item", back_populates="to_donor")
    to_donor_weight = relationship("DonorWeight", back_populates="to_donor")

class Item(Base):
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    item_points = Column(Integer, nullable=False)
    item_quantity = Column(Integer, nullable=False, default=0)
    item_barcode = Column(String, nullable=False)
    donor_id = Column(Integer, ForeignKey("donor.donor_id"))

    to_donor = relationship("Donor", back_populates="to_item")
    to_replenishment_item = relationship("ReplenishmentItem", back_populates="to_item")
    to_transaction_item = relationship("TransactionItem", back_populates="to_item")

class Manager(Base):
    __tablename__ = "manager"

    manager_id = Column(Integer, primary_key=True)
    manager_name = Column(String, unique=True, nullable=False)
    passhash = Column(String, nullable=False)

    to_replenishment = relationship("Replenishment", back_populates="to_manager")
    to_transaction = relationship("Transaction", back_populates="to_manager")

class Replenishment(Base):
    __tablename__ = "replenishment"

    replenish_id = Column(Integer, primary_key=True)
    replenish_time = Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey("manager.manager_id"))

    to_manager = relationship("Manager", back_populates="to_replenishment")
    to_replenishment_item = relationship("ReplenishmentItem", back_populates="to_replenishment")

class ReplenishmentItem(Base):
    __tablename__ = "replenishment_item"

    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    replenish_id = Column(Integer, ForeignKey("replenishment.replenish_id"), primary_key=True)
    replenish_quantity = Column(Integer, nullable=False)

    to_item = relationship("Item", back_populates="to_replenishment_item")
    to_replenishment = relationship("Replenishment", back_populates="to_replenishment_item")

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, primary_key=True)
    transaction_time = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey("manager.manager_id"))

    to_manager = relationship("Manager", back_populates="to_transaction")
    to_transaction_item = relationship("TransactionItem", back_populates="to_transaction")
    to_donor_weight = relationship("DonorWeight", back_populates="to_transaction")

class TransactionItem(Base):
    __tablename__ = "transaction_item"

    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.transaction_id"), primary_key=True)
    transaction_quantity = Column(Integer, nullable=False)

    to_item = relationship("Item", back_populates="to_transaction_item")
    to_transaction = relationship("Transaction", back_populates="to_transaction_item")

class DonorWeight(Base):
    __tablename__ = "donor_weight"
    
    donor_id = Column(Integer, ForeignKey("donor.donor_id"), primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.transaction_id"), primary_key=True)
    weight = Column(Float, nullable=False, default=0.0)

    to_transaction = relationship("Transaction", back_populates="to_donor_weight")
    to_donor = relationship("Donor", back_populates="to_donor_weight")
    