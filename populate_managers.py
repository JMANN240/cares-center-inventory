import crud
import schemas
from database import SessionLocal

def populate_managers():
    with SessionLocal() as db:
        crud.create_manager(db, schemas.ManagerCreate(manager_firstname="fn", manager_lastname="ln", manager_username="admin", password="test"))
        crud.create_manager(db, schemas.ManagerCreate(manager_firstname="Riley", manager_lastname="Libens", manager_username="rlibens", password="rlib"))
        crud.create_manager(db, schemas.ManagerCreate(manager_firstname="JT", manager_lastname="Raber", manager_username="jraber", password="jrab"))
        crud.create_manager(db, schemas.ManagerCreate(manager_firstname="Jason", manager_lastname="Abounader", manager_username="jabounader", password="jabo"))
        crud.create_manager(db, schemas.ManagerCreate(manager_firstname="Song", manager_lastname="Li", manager_username="sli", password="sli"))
        crud.create_manager(db, schemas.ManagerCreate(manager_firstname="Ty", manager_lastname="Poorman", manager_username="tpoorman", password="tpoo"))

if __name__ == '__main__':
    populate_managers()