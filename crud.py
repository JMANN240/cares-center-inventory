from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models, schemas
from random import randint
from passlib.hash import pbkdf2_sha256
import time

# manager
def create_manager(db: Session, manager: schemas.ManagerCreate):
    db_manager = models.Manager(
        manager_name = manager.manager_name,
        passhash = pbkdf2_sha256.hash(manager.password)
    )
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

def get_manager_by_manager_name(db: Session, manager_name: str):
    db_manager = db.query(models.Manager).filter(models.Manager.manager_name == manager_name).one()
    return db_manager

def update_manager_name_by_manager_id(db: Session, manager_id: int, new_manager_name: str):
    db.query(models.Manager).filter(models.Manager.manager_id == manager_id).update({models.Manager.manager_name: new_manager_name})
    db.commit()

def get_managers(db: Session):
    return db.query(models.Manager).all()

def delete_manager_by_manager_id(db: Session, manager_id: int):
    manager_to_delete = db.query(models.Manager).filter(models.Manager.manager_id == manager_id).one()
    db.delete(manager_to_delete)
    db.commit()

# donor
def create_donor(db: Session, donor: schemas.DonorCreate):
    db_donor = models.Donor(
        donor_name = donor.donor_name
    )
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def get_donor_by_donor_name(db: Session, donor_name: str):
    return db.query(models.Donor).filter(models.Donor.donor_name == donor_name).one()

def get_donor_by_donor_id(db: Session, donor_id: int):
    return db.query(models.Donor).filter(models.Donor.donor_id == donor_id).one()

def get_donors(db: Session):
    return db.query(models.Donor).all()

def update_donor_name_by_donor_id(db: Session, donor_id: int, new_donor_name: str):
    db.query(models.Donor).filter(models.Donor.donor_id == donor_id).update({models.Donor.donor_name: new_donor_name})
    db.commit()

def delete_donor_by_donor_id(db: Session, donor_id: int):
    donor_to_delete = db.query(models.Donor).filter(models.Donor.donor_id == donor_id).one()
    db.delete(donor_to_delete)
    db.commit()

# item
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
    
def get_item_by_item_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.item_id == item_id).one()

def get_items_by_donor_id(db: Session, donor_id: int):
    return db.query(models.Item).filter(models.Item.donor_id == donor_id).all()

def get_items_by_donor_name(db: Session, donor_name: str):
    return db.query(models.Item).join(models.Donor).filter(models.Donor.donor_name == donor_name).all()

def get_items_by_point_interval(db: Session, lhs: int, rhs: int):
    return db.query(models.Item).filter(and_(models.Item.item_points >= lhs, models.Item.item_points <= rhs)).all()

def get_item_by_item_barcode(db: Session, barcode: str):
    return db.query(models.Item).filter(models.Item.item_barcode == barcode).one()

def update_item_name_by_item_id(db: Session, item_id: int, new_item_name: str):
    db.query(models.Item).filter(models.Item.item_id == item_id).update({models.Item.item_name: new_item_name})
    db.commit()

def update_item_front_quantity_by_item_id(db: Session, item_id: int, new_item_front_quantity):
    db.query(models.Item).filter(models.Item.item_id == item_id).update({models.Item.item_front_quantity: new_item_front_quantity})
    db.commit()

def update_item_back_quantity_by_item_id(db: Session, item_id: int, new_item_back_quantity):
    db.query(models.Item).filter(models.Item.item_id == item_id).update({models.Item.item_back_quantity: new_item_back_quantity})
    db.commit()

def delete_item_by_item_id(db: Session, item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.item_id == item_id).one()
    db.delete(item_to_delete)
    db.commit()

# replenishment
def create_replenishment(db: Session, replenishment: schemas.ReplenishmentCreate):
    db_replenishment = models.Replenishment(
        replenish_time = int(time.time()),
        manager_id = replenishment.manager_id,
    )
    db.add(db_replenishment)
    db.commit()
    db.refresh(db_replenishment)
    return db_replenishment

def get_replenishments(db: Session):
    return db.query(models.Replenishment).all()

def get_replenishment_by_replenish_id(db: Session, replenish_id: int):
    return db.query(models.Replenishment).filter(models.Replenishment.replenish_id == replenish_id).one()

def get_replenishments_by_replenish_time_interval(db: Session, start_time: int, end_time: int):
    db_replenishments = db.query(models.Replenishment).all()
    result_lst = []
    
    for db_replenishment in db_replenishments:
        replenishment_time = db_replenishment.replenish_time
        if start_time <= replenishment_time and replenishment_time <= end_time:
            result_lst.append(db_replenishment)

    return result_lst

def get_replenishments_by_manager_id(db: Session, manager_id: int):
    return db.query(models.Replenishment).filter(models.Replenishment.manager_id == manager_id).all()

def delete_replenishment_by_replenish_id(db: Session, replenish_id: int):
    replenishment_to_delete = db.query(models.Replenishment).filter(models.Replenishment.replenish_id == replenish_id).one()
    db.delete(replenishment_to_delete)
    db.commit()

# replenishment_item
def create_replenishment_item(db: Session, replenishment_item = schemas.ReplenishmentItemCreate):
    db_replenishment_item = models.ReplenishmentItem(
        item_id = replenishment_item.item_id,
        replenish_id = replenishment_item.replenish_id,
        replenish_quantity = replenishment_item.replenish_quantity
    )
    db.add(db_replenishment_item)
    db.commit()
    db.refresh(db_replenishment_item)

def get_replenishment_items_by_replenish_id(db: Session, replenish_id: int):
    return db.query(models.ReplenishmentItem).filter(models.ReplenishmentItem.replenish_id == replenish_id).all()

def delete_replenishment_item_by_replenish_id_and_item_id(db: Session, replenish_id: int, item_id: int):
    replenishment_items_to_delete = db.query(models.ReplenishmentItem).filter(and_(models.ReplenishmentItem.replenish_id == replenish_id, models.ReplenishmentItem.item_id == item_id)).all()
    for replenishment_item in replenishment_items_to_delete:
        db.delete(replenishment_item)
    db.commit()

# transaction
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        transaction_time = int(time.time()),
        customer_id = transaction.customer_id,
        manager_id = transaction.manager_id,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session):
    return db.query(models.Transaction).all()

def get_transactions_by_transaction_time_interval(db: Session, start_time: int, end_time: int):
    db_transactions = db.query(models.Transaction).all()
    result_lst = []
    
    for db_transaction in db_transactions:
        transaction_time = db_transaction.replenish_time
        if start_time <= transaction_time and transaction_time <= end_time:
            result_lst.append(db_transaction)

    return result_lst

def get_transactions_by_customer_id(db: Session, customer_id: int):
    return db.query(models.Transaction).filter(models.Transaction.customer_id == customer_id).all()

def get_transaction_points_by_transaction_id(db: Session, transaction_id: int):
    transaction_items = get_transaction_items_by_transaction_id(db, transaction_id)

    transaction_points = 0
    for transaction_item in transaction_items:
        transaction_points += get_item_by_item_id(db, transaction_item.item_id).item_points
    return 

def  get_transactions_by_transaction_time_interval_and_customer_id(db: Session, start_time: int, end_time: int, customer_id: int):
    db_transactions = db.query(models.Transaction).filter(models.Transaction.customer_id == customer_id).all()
    result_lst = []
    
    for db_transaction in db_transactions:
        transaction_time = db_transaction.transaction_time
        if start_time <= transaction_time and transaction_time <= end_time:
            result_lst.append(db_transaction)

    return result_lst

def get_transactions_by_manager_id(db: Session, manager_id: int):
    return db.query(models.Transaction).filter(models.Transaction.manager_id == manager_id).all()

def delete_transaction_by_transaction_id(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).one()
    db.delete(transaction)
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
    return db_transaction_item

def get_transaction_items_by_transaction_id(db: Session, transaction_id: int):
    return db.query(models.TransactionItem).filter(models.TransactionItem.transaction_id == transaction_id).all()

def delete_transaction_items_by_transaction_id_and_item_id(db: Session, transaction_id: int, item_id: int):
    transaction_items_to_delete = db.query(models.TransactionItem).filter(and_(models.TransactionItem.transaction_id == transaction_id, models.TransactionItem.item_id == item_id)).all()
    for transaction_item in transaction_items_to_delete:
        db.delete(transaction_item)
    db.commit()

# donor_weight
def create_donor_weight(db: Session, donor_weight:schemas.DonorWeightCreate):
    db_donor_weight = models.DonorWeight(
        donor_id = donor_weight.donor_id,
        transaction_id = donor_weight.transaction_id,
        weight = donor_weight.weight
    )
    db.add(db_donor_weight)
    db.commit()
    db.refresh(db_donor_weight)
    return db_donor_weight

def get_donor_weights_by_transaction_id(db: Session, transaction_id: int):
    return db.query(models.DonorWeight).filter(models.DonorWeight.transaction_id == transaction_id).all()

def get_donor_weights_by_donor_id(db: Session, donor_id: int):
    return db.query(models.DonorWeight).filter(models.DonorWeight.donor_id == donor_id).all()

def get_donor_weights_by_transaction_time_interval(db: Session, start_time: int, end_time: int):
    db_donor_weights = db.query(models.DonorWeight).all()
    result_lst = []
    
    for db_donor_weight in db_donor_weights:
        donor_weight_time = db.query(models.Transaction).filter(models.Transaction.transaction_id == db_donor_weight.transaction_id).one().transaction_time
        if start_time <= donor_weight_time and donor_weight_time <= end_time:
            result_lst.append(db_donor_weight)

    return result_lst

def get_donor_weights_by_transaction_time_interval_and_donor_id(db: Session, start_time: int, end_time: int, donor_id: int):
    db_donor_weights = db.query(models.DonorWeight).filter(models.DonorWeight.donor_id == donor_id).all()
    result_lst = []
    
    for db_donor_weight in db_donor_weights:
        donor_weight_time = db.query(models.Transaction).filter(models.Transaction.transaction_id == db_donor_weight.transaction_id).one().transaction_time
        if start_time <= donor_weight_time and donor_weight_time<= end_time:
            result_lst.append(db_donor_weight)

    return result_lst

def delete_donor_weights_by_transaction_id_and_donor_id(db: Session, transaction_id: int, donor_id: int):
    donor_weights_to_delete = db.query(models.DonorWeight).filter(and_(models.DonorWeight.transaction_id == transaction_id, models.DonorWeight.donor_id == donor_id)).all()
    for donor_weight in donor_weights_to_delete:
        db.delete(donor_weight)
    db.commit()
