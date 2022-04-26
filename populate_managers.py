import crud
import schemas
from database import SessionLocal

def populate_managers():
    with SessionLocal() as db:
        crud.create_manager(db, schemas.ManagerCreate(firstname="fn", lastname="ln", username="admin", password="test", is_admin=True, is_active=True))
        crud.create_manager(db, schemas.ManagerCreate(firstname="Riley", lastname="Libens", username="rlibens", password="rlib", is_admin=True, is_active=True))
        crud.create_manager(db, schemas.ManagerCreate(firstname="JT", lastname="Raber", username="jraber", password="jrab", is_admin=True, is_active=True))
        crud.create_manager(db, schemas.ManagerCreate(firstname="Jason", lastname="Abounader", username="jabounader", password="jabo", is_admin=True, is_active=True))
        crud.create_manager(db, schemas.ManagerCreate(firstname="Song", lastname="Li", username="sli", password="sli", is_admin=False, is_active=True))
        crud.create_manager(db, schemas.ManagerCreate(firstname="Ty", lastname="Poorman", username="tpoorman", password="tpoo", is_admin=False, is_active=False))

if __name__ == '__main__':
    populate_managers()