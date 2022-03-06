from database import SessionLocal, engine
import models
import schemas
import crud

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# managers
manager_A = schemas.ManagerCreate(
    manager_name="manager_A",
    passcode="1111"
)

print("Creating manager with manager_name = manager_A:")
db_manager_A = crud.get_manager_by_username(db=db, username=manager_A.manager_name)

if db_manager_A is None:
    db_manager_A = crud.create_manager(db=db, manager=manager_A)
    print("  Manager was created successfully;")
else:
    print("  Manager already exists with manager_name = manager_A;")

manager_B = schemas.ManagerCreate(
    manager_name="manager_B",
    passcode="2222"
)

print("Creating manager with manager_name = manager_B:")
db_manager_B = crud.get_manager_by_username(db=db, username=manager_B.manager_name)

if db_manager_B is None:
    db_manager_B = crud.create_manager(db=db, manager=manager_A)

print("Updating manager name with manager_id = manager_B")
if crud.verify_manager(db=db, username="manager_A", password="1111"):
    if crud.get_manager_by_username(db=db, username="manager_B") is None:
        crud.update_manager_name_by_manager_id(db=db, manager_id=db_manager_A.manager_id, new_manager_name="manager_B")

# delete_manager_by_manager_id
if crud.get_manager_by_username(db=db, username=2) is not None:
    crud.delete_manager_by_manager_id(db=db, manager_id=2)

# ------------------------- donors -------------------------
donor_A = schemas.DonorCreate(
    donor_name="donor_A"
)

# get_donor_by_donor_name
db_donor_A = crud.get_donor_by_donor_name(db=db, donor_name=donor_A.donor_name)

# create_donor
if db_donor_A is None:
     db_donor_A = crud.create_donor(db=db, donor=donor_A)

Star_Bucks_donor = schemas.DonorCreate(
    donor_name="Star Bucks"
)

db_Star_Bucks_donor = crud.get_donor_by_donor_name(db=db, donor_name=Star_Bucks_donor.donor_name)

if db_Star_Bucks_donor is None:
    db_Star_Bucks_donor = crud.create_donor(db=db, donor=Star_Bucks_donor)

# update_donor_name_by_donor_id
if crud.get_donor_by_donor_name(db=db, donor_name="Flashes Fighting Hunger") is None:
    crud.update_donor_name_by_donor_id(db=db, donor_id=db_donor_A.donor_id, new_donor_name="Flashes Fighting Hunger")

# delete_donor_by_donor_name
if crud.get_donor_by_donor_name(db=db, donor_name="Star Bucks"):
    crud.delete_donor_by_donor_name(db=db, donor_name="Star Bucks")

# items
item_apple = schemas.ItemCreate(
    item_name="Apple",
    item_points=10,
    item_front_quantity=100,
    donor_id=db_donor_A.donor_id
)

crud.create_item(db=db, item=item_apple)

items = crud.get_items_by_donor_name(db=db, donor_name="donor_A")

for item in items:
    print(item.item_name)