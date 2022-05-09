from pydantic import BaseModel, validator
from typing import Optional, List

# Item
class ItemBase(BaseModel):
    name: str
    points: int
    quantity: int = 0
    donor_id: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    barcode: str

    class Config:
        orm_mode = True



# Donor
class DonorBase(BaseModel):
    name: str
    weighs: bool = False

class DonorCreate(DonorBase):
    pass

class Donor(DonorBase):
    id: int

    class Config:
        orm_mode = True



# Manager
class ManagerBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    is_admin: bool = False
    is_active: bool = True

class ManagerCreate(ManagerBase):
    password: str

class Manager(ManagerBase):
    id: int
    passhash: str

    class Config:
        orm_mode = True




# Transaction
class TransactionBase(BaseModel):
    student_id: int
    manager_id: int

class TransactionCreate(TransactionBase):
    pass
    
class Transaction(TransactionBase):
    time: int
    id: int

    class Config:
        orm_mode = True



# TransactionItem
class TransactionItemBase(BaseModel):
    item_id: int
    transaction_id: int
    quantity: int

class TransactionItemCreate(TransactionItemBase):
    pass

class TransactionItem(TransactionItemBase):
    pass

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



# Now with relationships for reading

class ItemRead(Item):
    donor: Donor

    class Config:
        orm_mode = True

class DonorRead(Donor):
    items: List[Item]
    weights: List[DonorWeight]

    class Config:
        orm_mode = True

class ManagerRead(Manager):
    transactions: List[Transaction]

    class Config:
        orm_mode = True

class TransactionItemRead(TransactionItem):
    item: ItemRead
    transaction: Transaction

class DonorWeightRead(DonorWeight):
    transaction: Transaction
    donor: Donor

    class Config:
        orm_mode = True

class TransactionRead(Transaction):
    manager: Manager
    items: List[TransactionItemRead]
    weights: List[DonorWeightRead]

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