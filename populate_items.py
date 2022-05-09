import crud
import schemas
from database import SessionLocal

def populate_items():
    with SessionLocal() as db:
        crud.create_item(db, schemas.ItemCreate(name="Beans", points=5, quantity=10, donor_id=1))
        crud.create_item(db, schemas.ItemCreate(name="Cake pop", points=10, quantity=10, donor_id=1))
        crud.create_item(db, schemas.ItemCreate(name="Bread", points=2, quantity=10, donor_id=2))

if __name__ == '__main__':
    populate_items()