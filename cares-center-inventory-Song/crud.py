from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models, schemas
from random import randint

# managers
def create_manager(db: Session, manager: schemas.ManagerCreate):
    db_manager = models.Manager(
        manager_name = manager.manager_name,
        passcode = manager.passcode
    )
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

def get_manager_by_username(db: Session, username: str):
    db_manager = db.query(models.Manager).filter(or_(models.Manager.manager_id == username, models.Manager.manager_name == username)).first()
    return db_manager

def update_manager_name_by_manager_id(db: Session, manager_id: str, new_manager_name: str):
    db.query(models.Manager).filter(models.Manager.manager_id == manager_id).update({models.Manager.manager_name: new_manager_name})
    db.commit()

def get_managers(db: Session):
    return db.query(models.Manager).all()

def delete_manager_by_manager_id(db: Session, manager_id: str):
    manager_to_delete = db.query(models.Manager).filter(models.Manager.manager_id == manager_id).first()
    db.delete(manager_to_delete)
    db.commit()

def verify_manager(db: Session, username: str, password: str):
    manager_found =  db.query(models.Manager).filter(and_(or_(models.Manager.manager_id == username, models.Manager.manager_name == username), models.Manager.passcode == password)).first()
    return False if not manager_found else True

# donors
def create_donor(db: Session, donor: schemas.DonorCreate):
    db_donor = models.Donor(
        donor_name = donor.donor_name
    )
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def get_donor_by_donor_name(db: Session, donor_name: str):
    return db.query(models.Donor).filter(models.Donor.donor_name == donor_name).first()

def get_donors(db: Session):
    return db.query(models.Donor).all()

def update_donor_name_by_donor_id(db: Session, donor_id: str, new_donor_name: str):
    db.query(models.Donor).filter(models.Donor.donor_id == donor_id).update({models.Donor.donor_name: new_donor_name})
    db.commit()

def delete_donor_by_donor_name(db: Session, donor_name: str):
    donor_to_delete = db.query(models.Donor).filter(models.Donor.donor_name == donor_name).first()
    db.delete(donor_to_delete)
    db.commit()

# items
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
        #item_back_quantity = item.item_back_quantity,
        donor_id = item.donor_id,
        item_barcode = new_barcode
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Item).all()
    
def get_items_by_donor_id(db: Session, donor_id: str):
    return db.query(models.Item).filter(models.Item.donor_id == donor_id).all()

def get_items_by_donor_name(db: Session, donor_name: str):
    return db.query(models.Item).join(models.Donor).filter(models.Donor.donor_name == donor_name).all()

def get_items_by_point_interval(db: Session, lhs: int, rhs: int):
    return db.query(models.Item).filter(and_(models.Item.item_points >= lhs, models.Item.item_points <= rhs)).all()

def update_item_name_by_item_id(db: Session, item_id: str, new_item_name: str):
    db.query(models.Item).filter(models.Item.item_id == item_id).update({models.Item.item_name: new_item_name})
    db.commit()

def update_item_front_quantity_by_item_id(db: Session, item_id: str, new_item_front_quantity):
    db.query(models.Item).filter(models.Item.item_id == item_id).update({models.Item.item_front_quantity: new_item_front_quantity})
    db.commit()

def delete_item_by_item_id(db: Session, item_id: str):
    item_to_delete = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    db.delete(item_to_delete)
    db.commit()

# replenish_history
def create_replenish_history(db: Session, replenish_history: schemas.ReplenishHistoryCreate):
    db_replenish_history = models.ReplenishHistory(
        replenish_date = replenish_history.replenish_date,
        manager_id = replenish_history.manager_id,
    )
    db.add(db_replenish_history)
    db.commit()
    db.refresh(db_replenish_history)
    return db_replenish_history

def get_replenish_history_by_replenish_id(db: Session, replenish_id: str):
    return db.query(models.ReplenishHistory).filter(models.ReplenishHistory.replenish_id == replenish_id).first()

def get_replenish_histories_by_replenish_date(db: Session, replenish_date: str):
    return db.query(models.ReplenishHistory).filter(models.ReplenishHistory.replenish_date == replenish_date).all()

def get_replenish_histories_by_manager_id(db: Session, manager_id: str):
    return db.query(models.ReplenishHistory).filter(models.ReplenishHistory.manager_id == manager_id).all()

def delete_replenish_history_by_replenish_id(db: Session, replenish_id: str):
    replenish_history_to_delete = db.query(models.ReplenishHistory).filter(models.ReplenishHistory.replenish_id == replenish_id).first()
    db.delete(replenish_history_to_delete)
    db.commit()

# replenish_item
def create_replenish_item(db: Session, replenish_item = schemas.ReplenishItemCreate):
    db_replenish_item = models.ReplenishItem(
        item_id = replenish_item.item_id,
        replenish_id = replenish_item.replenish_id,
        replenish_quantity = replenish_item.replenish_quantity
    )
    db.add(db_replenish_item)
    db.commit()
    db.refresh(db_replenish_item)

def get_replenish_items_by_replenish_id(db: Session, replenish_id: str):
    return db.query(models.ReplenishItem).filter(models.ReplenishItem.replenish_id == replenish_id).all()

def delete_replenish_items_by_item_id(db: Session, item_id: str):
    replenish_item_to_delete = db.query(models.ReplenishItem).filter(models.ReplenishItem.item_id == item_id).all()
    db.delete(replenish_item_to_delete)
    db.commit()

def delete_replenish_items_by_replenish_id(db: Session, replenish_id: str):
    replenish_item_to_delete = db.query(models.ReplenishItem).filter(models.ReplenishItem.replenish_id == replenish_id).all()
    db.delete(replenish_item_to_delete)
    db.commit()
 
# transaction_history
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

def get_transaction_histories_by_transaction_date(db: Session, transaction_date: str):
    return db.query(models.TransactionHistory).filter(models.TransactionHistory.transaction_date == transaction_date).all()

def get_transaction_histories_by_customer_id(db: Session, customer_id: str):
    return db.query(models.TransactionHistory).filter(models.TransactionHistory.customer_id == customer_id).all()

def  get_transaction_histories_by_transaction_date_and_customer_id(db: Session, transaction_date: str, customer_id: str):
    return db.query(models.TransactionHistory).filter(and_(models.TransactionHistory.transaction_date == transaction_date, models.TransactionHistory.customer_id == customer_id)).all()

def get_transaction_histories_by_manager_id(db: Session, manager_id: str):
    return db.query(models.TransactionHistory).filter(models.TransactionHistory.manager_id == manager_id).all()

def delete_transaction_history_by_transaction_id(db: Session, transaction_id: str):
    transaction_history_to_delete = db.query(models.TransactionHistory).filter(models.TransactionHistory.transaction_id == transaction_id).first()
    db.delete(transaction_history_to_delete)
    db.commit()

# transaction_items
def create_transaction_item(db: Session, transaction_item = schemas.TransactionItemCreate):
    db_transaction_item = models.TransactionItem(
        item_id = transaction_item.item_id,
        transaction_id = transaction_item.transaction_id,
        transaction_quantity = transaction_item.transaction_quantity
    )
    db.add(db_transaction_item)
    db.commit()
    db.refresh(db_transaction_item)

def get_transaction_items_by_transaction_id(db: Session, transaction_id: str):
    return db.query(models.TransactionItem).filter(models.TransactionItem.transaction_id == transaction_id).all()

def delete_transaction_items_by_item_id(db: Session, item_id: str):
    transaction_item_to_delete = db.query(models.TransactionItem).filter(models.TransactionItem.item_id == item_id).all()
    db.delete(transaction_item_to_delete)
    db.commit()

def delete_transaction_items_by_transaction_id(db: Session, transaction_id: str):
    transaction_item_to_delete = db.query(models.TransactionItem).filter(models.TransactionItem.transaction_id == transaction_id).all()
    db.delete(transaction_item_to_delete)
    db.commit()

# donor_weight
def create_donor_weight(db: Session, donor_weight:schemas.DonorWeightCreate):
    db_donor_weight = models.DonorWeight(
        donor_id = donor_weight.donor_id,
        transaction_id = donor_weight.transaction_id,
        weight = donor_weight.donor_id
    )
    db.add(db_donor_weight)
    db.commit()
    db.refresh(db_donor_weight)

def get_donor_weights_by_transaction_id(db: Session, transaction_id: str):
    return db.query(models.DonorWeight).filter(models.DonorWeight.transaction_id == transaction_id).all()

def get_donor_weights_by_donor_id(db: Session, donor_id: str):
    return db.query(models.DonorWeight).filter(models.DonorWeight.donor_id == donor_id).all()

def get_donor_weights_by_transaction_date(db: Session, transaction_date: str):
    return db.query(models.DonorWeight).join(models.TransactionHistory).filter(models.TransactionHistory.transaction_date == transaction_date).all()

def get_donor_weights_by_donor_id_and_transaction_date(db: Session, donor_id: str, transaction_date: str):
    return db.query(models.DonorWeight).join(models.TransactionHistory).filter(and_(models.DonorWeight.donor_id == donor_id, models.TransactionHistory.transaction_date == transaction_date)).all()

def delete_donor_weights_by_donor_id(db: Session, donor_id: str):
    donor_weight_to_delete = db.query(models.DonorWeight).filter(models.DonorWeight.donor_id == donor_id).all()
    db.delete(donor_weight_to_delete)
    db.commit()

def delete_donor_weights_by_transaction_id(db: Session, transaction_id: str):
    donor_weight_to_delete = db.query(models.DonorWeight).filter(models.DonorWeight.transaction_id == transaction_id).all()
    db.delete(donor_weight_to_delete)
    db.commit()