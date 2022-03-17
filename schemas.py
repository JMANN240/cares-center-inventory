from pydantic import BaseModel, validator
from typing import Optional, List

from main import replenish, transaction

# Manager
class ManagerBase(BaseModel):
    manager_firstname: str
    manager_lastname: str
    manager_username: str
    is_admin: bool

class ManagerCreate(ManagerBase):
    password: str # When creating a manager it takes the actual password to hash and then store

class Manager(ManagerBase):
    manager_id: int
    passhash: str # But when returning a manager it returns the stored hash
    is_active: bool

    class Config:
        orm_mode = True

# Donor
class DonorBase(BaseModel):
    donor_name: str

class DonorCreate(DonorBase):
    pass

class Donor(DonorBase):
    donor_id: int

    class Config:
        orm_mode = True

# Item
class ItemBase(BaseModel):
    item_name: str
    item_points: int
    item_quantity: int = 0
    donor_id: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int
    item_barcode: str

    class Config:
        orm_mode = True

# ReplensihmentItem
class ReplenishmentItemBase(BaseModel):
    item_id: int
    replenish_id: int
    replenish_quantity: int

class ReplenishmentItemCreate(ReplenishmentItemBase):
    pass

class ReplensihmentItem(ReplenishmentItemBase):
    pass

    class Config:
        orm_mode = True

# Replenishment
class ReplenishmentBase(BaseModel):
    manager_id: int

class ReplenishmentCreate(ReplenishmentBase):
    pass

class Replenishment(ReplenishmentBase):
    replenish_time: int
    replenish_id: int

    class Config:
        orm_mode = True

# TransactionItem
class TransactionItemBase(BaseModel):
    item_id: int
    transaction_id: int
    transaction_quantity: int

class TransactionItemCreate(TransactionItemBase):
    pass

class TransactionItem(TransactionItemBase):
    pass

    class Config:
        orm_mode = True

# Transaction
class TransactionBase(BaseModel):
    customer_id: int
    manager_id: int

class TransactionCreate(TransactionBase):
    pass
    
class Transaction(TransactionBase):
    transaction_time: int
    transaction_id: int

    class Config:
        orm_mode = True

# DonorWeight
class DonorWeightBase(BaseModel):
    donor_id: int
    transaction_id: int
    weight: float

class DonorWeightCreate(DonorWeightBase):
    pass

class DonorWeight(DonorWeightBase):
    pass

    class Config:
        orm_mode = True

# Barcodes

class Barcode(BaseModel):
    data: str
    name: Optional[str]

    @validator('data')
    def data_must_be_7_chars(cls, d):
        if len(d) != 7:
            raise ValueError("EAN-8 barcode data must contain only 7 characters")
        return d
    
    @validator('data')
    def data_must_be_numeric(cls, d):
        if not d.isdecimal():
            raise ValueError("EAN-8 barcode data must contain only numbers")
        return d

# Logging in

class Login(BaseModel):
    username: str
    password: str

# Creating replenishments and transactions

class ReplenishWithItems(BaseModel):
    replenish: ReplenishmentCreate
    replenish_items: List[ReplenishmentItemCreate]

class TransactionWithItems(BaseModel):
    transaction: TransactionCreate
    transaction_items: List[TransactionItemCreate]