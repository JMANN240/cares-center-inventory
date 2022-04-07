from io import BytesIO
from xmlrpc.client import ResponseError
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import barcode as bc
from barcode.writer import ImageWriter
import crud
import models
import schemas
from database import SessionLocal, engine
import sqlalchemy
from sqlalchemy.orm import Session
from typing import List
from passlib.hash import pbkdf2_sha256
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Optional

db = SessionLocal()

manager1 = schemas.ManagerCreate(
    manager_firstname="manager",
    manager_lastname="1",
    password="manager1"
)
db_manager1 = crud.create_manager(db=db, manager=manager1)

donor1 = schemas.DonorCreate(
    donor_name="donor1"
)
db_donor1 = crud.create_donor(db=db, donor=donor1)

item1 = schemas.ItemCreate(
    item_name="item1",
    item_points=1,
    item_quantity=10,
    donor_id=db_donor1.donor_id
)
crud.create_item(db=db, item=item1)

transaction1 = schemas.TransactionCreate(
    customer_id=1,
    manager_id=db_manager1.manager_id
)
db_transaction1 = crud.create_transaction(db=db, transaction=transaction1)

#crud.delete_transaction_by_transaction_id(db=db, transaction_id=db_transaction1.transaction_id)
crud.delete_manager_by_manager_id(db=db, manager_id=db_manager1.manager_id)