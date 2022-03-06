from pydantic import BaseModel, validator
from typing import Optional

# Manager
class ManagerBase(BaseModel):
    manager_name: str
    passcode: int

class ManagerCreate(ManagerBase):
    pass

class ManagerDelete(ManagerBase):
    pass

class Manager(ManagerBase):
    manager_id:int

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
    item_front_quantity: int
    #item_back_quantity: int
    donor_id: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int
    item_barcode: str

    class Config:
        orm_mode = True

# ReplenishItem
class ReplenishItemBase(BaseModel):
    item_id: int
    replenish_id: int
    replenish_quantity: int

class ReplenishItemCreate(ReplenishItemBase):
    pass

class ReplenishItem(ReplenishItemBase):
    pass

    class Config:
        orm_mode = True

# ReplenishHistory
class ReplenishHistoryBase(BaseModel):
    replenish_date: str
    manager_id: int

class ReplenishHistoryCreate(ReplenishHistoryBase):
    pass

class ReplenishHistory(ReplenishHistoryBase):
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

# TransactionHistory
class TransactionHistoryBase(BaseModel):
    transaction_date: str
    transaction_points: int
    customer_id: int
    manager_id: int

class TransactionHistoryCreate(TransactionHistoryBase):
    pass
    
class TransactionHistory(TransactionHistoryBase):
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