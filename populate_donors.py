import crud
import models
import schemas
from database import SessionLocal

with SessionLocal() as db:
    crud.create_donor(db, schemas.DonorCreate(donor_name="Starbucks"))
    crud.create_donor(db, schemas.DonorCreate(donor_name="FFH"))