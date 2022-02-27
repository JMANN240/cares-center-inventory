from pydantic import BaseModel, validator
from typing import Optional



class DonorBase(BaseModel):
    donor_name: str

class DonorCreate(DonorBase):
    pass

class Donor(DonorBase):
    donor_id: int

    class Config:
        orm_mode = True



class ItemBase(BaseModel):
    item_name: str
    item_points: int
    item_front_quantity: int
    item_back_quantity: int
    donor_id: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int
    item_barcode: str

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