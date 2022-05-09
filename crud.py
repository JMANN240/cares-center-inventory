from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models, schemas
from random import randint
from passlib.hash import pbkdf2_sha256
import time



# manager
def create_manager(db: Session, manager: schemas.ManagerCreate):
    manager_dict = manager.dict()
    del manager_dict['password']
    db_manager = models.Manager(
        passhash = pbkdf2_sha256.hash(manager.password),
        **manager_dict
    )
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

def get_managers(db: Session):
    return db.query(models.Manager).all()

def get_manager_by_username(db: Session, username: str):
    db_manager = db.query(models.Manager).filter(models.Manager.username == username).one()
    return db_manager

def get_manager_by_id(db: Session, id: int):
    db_manager = db.query(models.Manager).filter(models.Manager.id == id).one()
    return db_manager

def update_manager(db: Session, manager: schemas.Manager):
    db.query(models.Manager).filter(models.Manager.id == manager.id).update(manager.dict())
    db.commit()



# donor
def create_donor(db: Session, donor: schemas.DonorCreate):
    db_donor = models.Donor(
        **donor.dict()
    )
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def get_donors(db: Session):
    return db.query(models.Donor).all()

def get_donor_by_id(db: Session, id: int):
    return db.query(models.Donor).filter(models.Donor.id == id).one()

def update_donor(db: Session, donor: schemas.Donor):
    db.query(models.Donor).filter(models.Donor.id == donor.id).update(donor.dict())
    db.commit()



# item
def create_item(db: Session, item: schemas.ItemCreate):
    barcodes = [item.barcode for item in db.query(models.Item).all()]
    while True:
        new_barcode = str(randint(0, 9999999)).rjust(7, '0')
        if new_barcode not in barcodes:
            break

    db_item = models.Item(
        **item.dict(),
        barcode = new_barcode
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Item).all()
    
def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).one()

def get_items_by_donor_id(db: Session, donor_id: int):
    return db.query(models.Item).filter(models.Item.donor_id == donor_id).all()

def get_items_by_point_interval(db: Session, low: int, high: int):
    return db.query(models.Item).filter(and_(low <= models.Item.points, models.Item.points <= high)).all()

def get_item_by_barcode(db: Session, barcode: str):
    return db.query(models.Item).filter(models.Item.barcode == barcode).one()

def update_item(db: Session, item: schemas.Item):
    db.query(models.Item).filter(models.Item.id == item.id).update(item.dict())
    db.commit()

def update_item_quantity_by_id_relative(db: Session, id: int, quantity_delta: float):
    db.query(models.Item).filter(models.Item.id == id).update({models.Item.quantity: models.Item.quantity + quantity_delta})
    db.commit()



# transaction
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        **transaction.dict(),
        time = int(time.time())
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session):
    return db.query(models.Transaction).all()

def get_transaction_by_id(db: Session, id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == id).one()

def get_transactions_by_time_interval(db: Session, start: int, end: int):
    db_transactions = db.query(models.Transaction).all()
    result_lst = []
    
    for db_transaction in db_transactions:
        transaction_time = db_transaction.replenish_time
        if start <= transaction_time and transaction_time <= end:
            result_lst.append(db_transaction)

    return result_lst

def get_transactions_by_student_id(db: Session, student_id: int):
    return db.query(models.Transaction).filter(models.Transaction.student_id == student_id).all()

def get_transaction_points_by_id(db: Session, id: int):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == id).one()
    return sum([get_item_by_id(db, item.id).points for item in transaction.items])

def  get_transactions_by_time_interval_and_student_id(db: Session, start: int, end: int, student_id: int):
    db_transactions = db.query(models.Transaction).filter(models.Transaction.student_id == student_id).all()
    result_lst = []
    
    for db_transaction in db_transactions:
        transaction_time = db_transaction.transaction_time
        if start <= transaction_time and transaction_time <= end:
            result_lst.append(db_transaction)

    return result_lst

def get_transactions_by_manager_id(db: Session, manager_id: int):
    return db.query(models.Transaction).filter(models.Transaction.manager_id == manager_id).all()



# transaction_items
def create_transaction_item(db: Session, transaction_item = schemas.TransactionItemCreate):
    db_transaction_item = models.TransactionItem(
        **transaction_item.dict()
    )
    db.add(db_transaction_item)
    db.commit()
    db.refresh(db_transaction_item)
    return db_transaction_item

def get_transaction_items_by_transaction_id(db: Session, transaction_id: int):
    return db.query(models.TransactionItem).filter(models.TransactionItem.transaction_id == transaction_id).all()



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

def get_donor_weights_by_time_interval(db: Session, start: int, end: int):
    db_donor_weights = db.query(models.DonorWeight).all()
    result_lst = []
    
    for db_donor_weight in db_donor_weights:
        donor_weight_time = db.query(models.Transaction).filter(models.Transaction.transaction_id == db_donor_weight.transaction_id).one().transaction_time
        if start <= donor_weight_time and donor_weight_time <= end:
            result_lst.append(db_donor_weight)

    return result_lst

def get_donor_weights_by_time_interval_and_donor_id(db: Session, start: int, end: int, donor_id: int):
    db_donor_weights = db.query(models.DonorWeight).filter(models.DonorWeight.donor_id == donor_id).all()
    result_lst = []
    
    for db_donor_weight in db_donor_weights:
        donor_weight_time = db.query(models.Transaction).filter(models.Transaction.transaction_id == db_donor_weight.transaction_id).one().transaction_time
        if start <= donor_weight_time and donor_weight_time<= end:
            result_lst.append(db_donor_weight)

    return result_lst
