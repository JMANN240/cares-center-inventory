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
from passlib.hash import pbkdf2_sha256

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

@api.post("/manager/register", response_model=schemas.Manager)
def register_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db)):
    return crud.create_manager(db, manager=manager)

@api.post("/manager/login", response_model=bool)
def manager_login(username: str, password: str, db: Session = Depends(get_db)):
    global active_manager
    db_manager = crud.get_manager_by_manager_name(db, manager_name=username)
    is_password_correct = pbkdf2_sha256.verify(password, db_manager.passhash)
    if is_password_correct:
        active_manager = db_manager
    return False if active_manager is None else True

@api.post("/manager/logout")
def manager_logout():
    global active_manager
    active_manager = None

@api.get("/manager/read", response_model=List[schemas.Manager])
def read_managers(db: Session = Depends(get_db)):
    return crud.get_managers(db)

@api.get("/donor", response_model=List[schemas.Donor])
def read_donors(db: Session = Depends(get_db)):
    return crud.get_donors(db)

@api.post("/donor", response_model=schemas.DonorCreate)
def create_donor(donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    return crud.create_donor(db, donor=donor)

@api.get("/item", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@api.post("/item", response_model=schemas.ItemCreate)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)

@api.get("/barcode", status_code=200)
async def get_barcode(barcode: schemas.Barcode):
    barcodeImage = bc.get('ean8', barcode.data, writer=ImageWriter())
    barcodeFile = BytesIO()
    barcodeImage.write(barcodeFile, writerOptions)
    barcodeFile.seek(0)
    return StreamingResponse(barcodeFile, media_type='image/png')
    