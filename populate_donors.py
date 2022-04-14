import crud
import schemas
from database import SessionLocal

def populate_donors():
    with SessionLocal() as db:
        crud.create_donor(db, schemas.DonorCreate(donor_name="Starbucks"))
        crud.create_donor(db, schemas.DonorCreate(donor_name="FFH"))

if __name__ == '__main__':
    populate_donors()