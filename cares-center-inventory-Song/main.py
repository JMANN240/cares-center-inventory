from io import BytesIO
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import barcode as bc
from barcode.writer import ImageWriter
import crud
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from datetime import date

# Setup

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
api = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/api", api)

templates = Jinja2Templates(directory="templates")

writerOptions = {
    'text_distance': 1.0,
    'quiet_zone': 2.0,
    'background': '#ffffff',
    'foreground': '#000000',
}

# Front-end stuff

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/replenish")
async def replenish(request: Request):
    return templates.TemplateResponse("replenish.html", {"request": request})

@app.get("/transaction")
async def transaction(request: Request):
    return templates.TemplateResponse("transaction.html", {"request": request})

@app.get("/search")
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})



# Back-end

active_manager: schemas.Manager = None

@api.post("/managers/register", response_model=schemas.Manager)
def register_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db)):
    return crud.create_manager(db, manager=manager)

@api.get("/managers/login", response_model=bool)
def manager_login(username: str, password: str, db: Session = Depends(get_db)):
    global active_manager
    active_manager = crud.verify_manager(db, username=username, password=password)
    return False if active_manager is None else True

@api.post("/managers/logout")
def manager_logout():
    global active_manager
    active_manager = None

@api.get("/managers/read", response_model=List[schemas.Manager])
def read_managers(db: Session = Depends(get_db)):
    return crud.get_managers(db)

@api.delete("/manager/deregister")
def deregister_manager(username: str, password: str, db: Session = Depends(get_db)):
    crud.delete_manager(db, username=username, password=password)



@api.get("/donors", response_model=List[schemas.Donor])
def read_donors(db: Session = Depends(get_db)):
    return crud.get_donors(db)

@api.post("/donors", response_model=schemas.Donor)
def create_donor(donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    return crud.create_donor(db, donor=donor)



@api.get("/items", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@api.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)

@api.delete("/items")
def delete_items(db: Session = Depends(get_db)):
    crud.delete_items(db)
    return 200
    
"""
@api.post("/make_replenishment", response_model=schemas.ReplenishHistory)
def make_replenishment(barcodes: List[str], quantities: List[int], db: Session = Depends(get_db)):
    # create a replenish_history entity
    replenish_history = schemas.ReplenishHistoryCreate(
        replenish_date = str(date.today()),
        manager_id = active_manager.manager_id,
    )
    replenish_history: schemas.ReplenishHistory = crud.create_replenish_history(db, replenish_history=replenish_history)

    # create corresponding number of replenish_item entities
    for barcode, quantity in zip(barcodes, quantities):
        replenish_item = schemas.ReplenishItemCreate(
            item_id = db.query(models.Item).filter(models.Item.item_barcode == barcode).first().item_id,
            replenish_id = replenish_history.replenish_id,
            replenish_quantity = quantity
        )
        crud.create_replenish_item(db, replenish_item=replenish_item)

    return replenish_history

@api.post("/operate_transaction", response_model=schemas.TransactionHistory)
def operate_transaction(customer_id: int , barcodes: List[str], weights: List[float], db: Session = Depends(get_db)):
    # create a transaction_history entity
    transaction_points = 0
    for barcode in barcodes:
        transaction_points += db.query(models.Item).filter(models.Item.item_barcode == barcode).first().item_points
    
    transaction_history = schemas.TransactionHistoryCreate(
        transaction_date = str(date.today()),
        transaction_points = transaction_points,
        customer_id = customer_id,
        manager_id = active_manager.manager_id,
    )
    transaction_history: schemas.TransactionHistory = crud.create_transaction_history(db, transaction_history)

    # create corresponding number of transaction_item entities
    quantities = {i:barcodes.count(i) for i in set(barcodes)}
    for quantity in quantities:
        transaction_item = schemas.TransactionItemCreate(
            item_id = db.query(models.Item).filter(models.Item.item_barcode == barcode).first().item_id,
            transaction_id = transaction_history.transaction_id,
            transaction_quantity = quantities[barcode]
        )
        crud.create_transaction_item(db, transaction_item=transaction_item)

    # create corresponding number of donor weight entities
    donor_ids = [db.query(models.Item).filter(models.Item.item_barcode == barcode).first().donor_id for barcode in barcodes]

    for donor_id in set(donor_ids):
        donor_total_weight = 0
        for barcode, weight in zip(barcodes, weights):
            if db.query(models.Item).filter(models.Item.item_barcode == barcode).first().donor_id == donor_id:
                donor_total_weight += weight

        donor_weight = schemas.DonorWeightCreate(
            donor_id = donor_id,
            transaction_id = transaction_history.transaction_id,
            weight = donor_total_weight
        )
        crud.create_donor_weight(db, donor_weight=donor_weight)

    return transaction_history
"""

@api.get("/barcode", status_code=200)
async def get_barcode(barcode: schemas.Barcode):
    barcodeImage = bc.get('ean8', barcode.data, writer=ImageWriter())
    barcodeFile = BytesIO()
    barcodeImage.write(barcodeFile, writerOptions)
    barcodeFile.seek(0)
    return StreamingResponse(barcodeFile, media_type='image/png')