import crud
import schemas
from database import SessionLocal

def populate_transactions():
    with SessionLocal() as db:
        tx1 = crud.create_transaction(db, schemas.TransactionCreate(student_id=123, manager_id=1))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=1, transaction_id=tx1.id, quantity=1))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=2, transaction_id=tx1.id, quantity=2))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=3, transaction_id=tx1.id, quantity=3))
        crud.create_donor_weight(db, schemas.DonorWeightCreate(donor_id=1, transaction_id=tx1.id, weight=1.1))
        crud.create_donor_weight(db, schemas.DonorWeightCreate(donor_id=2, transaction_id=tx1.id, weight=1.2))

        tx2 = crud.create_transaction(db, schemas.TransactionCreate(student_id=456, manager_id=2))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=1, transaction_id=tx2.id, quantity=4))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=2, transaction_id=tx2.id, quantity=5))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=3, transaction_id=tx2.id, quantity=6))
        crud.create_donor_weight(db, schemas.DonorWeightCreate(donor_id=1, transaction_id=tx2.id, weight=2.1))
        crud.create_donor_weight(db, schemas.DonorWeightCreate(donor_id=2, transaction_id=tx2.id, weight=2.2))
        
        tx3 = crud.create_transaction(db, schemas.TransactionCreate(student_id=789, manager_id=3))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=1, transaction_id=tx3.id, quantity=7))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=2, transaction_id=tx3.id, quantity=8))
        crud.create_transaction_item(db, schemas.TransactionItemCreate(item_id=3, transaction_id=tx3.id, quantity=9))
        crud.create_donor_weight(db, schemas.DonorWeightCreate(donor_id=1, transaction_id=tx3.id, weight=3.1))
        crud.create_donor_weight(db, schemas.DonorWeightCreate(donor_id=2, transaction_id=tx3.id, weight=3.2))

if __name__ == '__main__':
    populate_transactions()