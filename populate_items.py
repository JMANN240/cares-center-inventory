import crud
import schemas
from database import SessionLocal

def populate_items():
    with SessionLocal() as db:
        crud.create_item(db, schemas.ItemCreate(item_name="Beans", item_points=5, item_quantity=10, donor_id=1))
        crud.create_item(db, schemas.ItemCreate(item_name="Cake pop", item_points=10, item_quantity=10, donor_id=1))
        crud.create_item(db, schemas.ItemCreate(item_name="Bread", item_points=2, item_quantity=10, donor_id=2))

if __name__ == '__main__':
    populate_items()