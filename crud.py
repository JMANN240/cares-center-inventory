from sqlalchemy.orm import Session
import models
import schemas
from random import randint

def get_donors(db: Session):
    return db.query(models.Donor).all()

def get_items(db: Session):
    return db.query(models.Item).all()
    
def get_items_by_donor(db: Session, donor_name: str):
    return db.query(models.Item).filter(models.Item.donor.donor_name == donor_name).all()

def create_donor(db: Session, donor: schemas.DonorCreate):
    db_donor = models.Donor(
        donor_name = donor.donor_name
    )
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def create_item(db: Session, item: schemas.ItemCreate):
    item_barcodes = [row[0] for row in db.query(models.Item.item_barcode).all()]
    print(item_barcodes)
    while True:
        new_barcode = str(randint(0, 9999999)).rjust(7, '0')
        print(f"trying {new_barcode}")
        if new_barcode not in item_barcodes:
            break

    db_item = models.Item(
        item_name = item.item_name,
        item_points = item.item_points,
        item_front_quantity = item.item_front_quantity,
        item_back_quantity = item.item_back_quantity,
        donor_id = item.donor_id,
        item_barcode = new_barcode
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_items(db: Session):
    items = get_items(db)
    for item in items:
        db.delete(item)
    db.commit()