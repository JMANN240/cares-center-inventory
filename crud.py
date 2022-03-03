from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models
import schemas
from random import randint

# ---------- managers ----------
def create_manager(db: Session, manager: schemas.ManagerCreate):
    db_manager = models.Manager(
        manager_name = manager.manager_name,
        passcode = manager.passcode
    )
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

def verify_manager(db: Session, username: str, password: str):
    return db.query(models.Manager).filter(and_(or_(models.Manager.manager_id == username, models.Manager.manager_name == username), models.Manager.passcode == password)).first()

def get_managers(db: Session):
    return db.query(models.Manager).all()

def delete_manager(db: Session, username: str, password: str):
    manager_to_delete = db.query(models.Manager).filter(and_(or_(models.Manager.manager_id == username, models.Manager.manager_name == username), models.Manager.passcode == password)).first()
    db.delete(manager_to_delete)
    db.commit()

# ---------- donors ----------
def create_donor(db: Session, donor: schemas.DonorCreate):
    db_donor = models.Donor(
        donor_name = donor.donor_name
    )
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def get_donors(db: Session):
    return db.query(models.Donor).all()

# ---------- items ----------
def create_item(db: Session, item: schemas.ItemCreate):
    item_barcodes = [item.item_barcode for item in db.query(models.Item).all()]
    while True:
        new_barcode = str(randint(0, 9999999)).rjust(7, '0')
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

def get_items(db: Session):
    return db.query(models.Item).all()
    
def get_items_by_donor_name(db: Session, donor_name: str):
    return db.query(models.Item).filter(models.Item.to_donor.donor_name == donor_name).all()

def delete_items(db: Session):
    items = get_items(db)
    for item in items:
        db.delete(item)
    db.commit()

# ---------- replenish_item ----------
def create_replenish_item(db: Session, replenish_item = schemas.ReplenishItemCreate):
    db_replenish_item = models.ReplenishItem(
        item_id = replenish_item.item_id,
        replenish_id = replenish_item.replenish_id,
        replenish_quantity = replenish_item.replenish_quantity
    )

    # update item quantity
    db.query(models.Item).filter(models.Item.item_id == replenish_item.item_id).update({models.Item.item_front_quantity: models.Item.item_front_quantity + replenish_item.replenish_quantity})
    
    db.add(db_replenish_item)
    db.commit()
    db.refresh(db_replenish_item)

def get_replenish_items(db: Session):
    return db.query(models.ReplenishItem).all()

# ---------- replenish_history ----------
def create_replenish_history(db: Session, replenish_history: schemas.ReplenishHistoryCreate):
    db_replenish_history = models.ReplenishHistory(
        replenish_date = replenish_history.replenish_date,
        manager_id = replenish_history.manager_id,
    )
    db.add(db_replenish_history)
    db.commit()
    db.refresh(db_replenish_history)
    return db_replenish_history

# ---------- transaction_items ----------
def create_transaction_item(db: Session, transaction_item = schemas.TransactionItemCreate):
    db_transaction_item = models.TransactionItem(
        item_id = transaction_item.item_id,
        transaction_id = transaction_item.transaction_id,
        transaction_quantity = transaction_item.transaction_quantity
    )
    
    # update item quantity
    db.query(models.Item).filter(models.Item.item_id == transaction_item.item_id).update({models.Item.item_front_quantity: models.Item.item_front_quantity - transaction_item.transaction_quantity})
    
    db.add(db_transaction_item)
    db.commit()
    db.refresh(db_transaction_item)
 
# ---------- transaction_history ----------
def create_transaction_history(db: Session, transaction_history: schemas.TransactionHistoryCreate):
    db_transaction_history = models.TransactionHistory(
        transaction_date = transaction_history.transaction_date,
        transaction_points = transaction_history.transaction_points,
        customer_id = transaction_history.customer_id,
        manager_id = transaction_history.manager_id,
    )
    db.add(db_transaction_history)
    db.commit()
    db.refresh(db_transaction_history)
    return db_transaction_history

# ---------- donor_weight ----------
def create_donor_weight(db: Session, donor_weight:schemas.DonorWeightCreate):
    db_donor_weight = models.DonorWeight(
        donor_id = donor_weight.donor_id,
        transaction_id = donor_weight.transaction_id,
        weight = donor_weight.donor_id
    )
    db.add(db_donor_weight)
    db.commit()
    db.refresh(db_donor_weight)