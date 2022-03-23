import crud
import models
import schemas
from database import SessionLocal

with SessionLocal() as db:
    crud.create_item(db, schemas.ItemCreate(item_name="Beans", item_points=5, item_front_quantity=10, item_back_quantity=5, donor_id=1))
    crud.create_item(db, schemas.ItemCreate(item_name="Cake pop", item_points=10, item_front_quantity=10, item_back_quantity=10, donor_id=1))
    crud.create_item(db, schemas.ItemCreate(item_name="Bread", item_points=2, item_front_quantity=10, item_back_quantity=10, donor_id=2))