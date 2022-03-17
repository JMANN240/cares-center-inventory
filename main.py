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

# Setup

models.Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    try:
        crud.get_manager_by_manager_username(db, "admin")
    except sqlalchemy.orm.exc.NoResultFound:
        crud.create_manager(
            db, 
            schemas.ManagerCreate(
                manager_firstname="fn",
                manager_lastname="ln",
                manager_username="admin",
                password="test",
                is_admin=True
            )
        )


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

# Middleware

def check_auth(route):
    async def modified_route(request: Request, user_id: Optional[int] = Cookie(None)):
        if user_id is not None or request.url.path == '/login':
            response = await route(request)
        else:
            response = RedirectResponse(f"/login?redirect={str(urlsafe_b64encode(bytes(request.url.path, encoding='utf-8')))[2:-1]}")
        return response
    return modified_route

# Front-end stuff

@app.get("/")
@check_auth
async def index(request: Request):
    print("in index")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/replenish")
@check_auth
async def replenish(request: Request):
    return templates.TemplateResponse("replenish.html", {"request": request})

@app.get("/transaction")
@check_auth
async def transaction(request: Request):
    return templates.TemplateResponse("transaction.html", {"request": request})

@app.get("/search")
@check_auth
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/barcode")
async def barcode(request: Request):
    return templates.TemplateResponse("barcode.html", {"request": request})



# Back-end

@api.post("/manager/register", response_model=schemas.Manager)
def register_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db)):
    return crud.create_manager(db, manager=manager)

@api.post("/manager/login")
def manager_login(login: schemas.Login, response: Response, db: Session = Depends(get_db)):
    try:
        db_manager = crud.get_manager_by_manager_username(db, manager_username=login.username)
        is_password_correct = pbkdf2_sha256.verify(login.password, db_manager.passhash)
    
        if is_password_correct:
            response.set_cookie(key="user_id", value=db_manager.manager_id, max_age=60*60*6)
            response.status_code = 200
            return response
        else:
            response.status_code = 406
            return response
    except sqlalchemy.exc.NoResultFound:
        response.status_code = 406
        return response

@api.post("/manager/logout")
def manager_logout(response: Response):
    response.set_cookie(key="user_id", value=None, max_age=0)
    response.status_code = 200
    return response

@api.get("/manager/read", response_model=List[schemas.Manager])
def read_managers(db: Session = Depends(get_db)):
    return crud.get_managers(db)

@api.get("/donor", response_model=List[schemas.Donor])
def read_donors(db: Session = Depends(get_db)):
    return crud.get_donors(db)

@api.post("/donor", response_model=schemas.Donor)
def create_donor(donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    return crud.create_donor(db, donor=donor)

@api.get("/item", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@api.post("/item", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)

@api.post("/transaction", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

@api.post("/transaction/item", response_model=schemas.TransactionItem)
def create_transaction_item(transaction_item: schemas.TransactionItemCreate, db: Session = Depends(get_db)):
    return crud.create_transaction_item(db, transaction_item)

@api.post("/transaction/items", response_model=List[schemas.TransactionItem])
def create_transaction_item(transaction_items: List[schemas.TransactionItemCreate], db: Session = Depends(get_db)):
    items = []
    for transaction_item in transaction_items:
        db_item = crud.create_transaction_item(db, transaction_item)
        items.append(db_item)
    return items

@api.post("/transaction/weight", response_model=schemas.DonorWeight)
def create_transaction_donor_weight(donor_weight: schemas.DonorWeightCreate, db: Session = Depends(get_db)):
    return crud.create_donor_weight(db, donor_weight)

@api.post("/transaction/weights", response_model=List[schemas.DonorWeight])
def create_transaction_donor_weights(donor_weights: List[schemas.DonorWeightCreate], db: Session = Depends(get_db)):
    weights = []
    for donor_weight in donor_weights:
        db_donor_weight = crud.create_donor_weight(db, donor_weight)
        weights.append(db_donor_weight)
    return weights

@api.post("/replenishment", response_model=schemas.Replenishment)
def create_replenishment(replenishment: schemas.ReplenishmentCreate, db: Session = Depends(get_db)):
    return crud.create_replenishment(db, replenishment)

@api.post("/replenishment/item", response_model=schemas.ReplensihmentItem)
def create_replenishment_item(replenishment_item: schemas.ReplenishmentItemCreate, db: Session = Depends(get_db)):
    return crud.create_replenishment_item(db, replenishment_item)

@api.post("/replenishment/items", response_model=List[schemas.ReplensihmentItem])
def create_replenishment_item(replenishment_items: List[schemas.ReplenishmentItemCreate], db: Session = Depends(get_db)):
    items = []
    for replenishment_item in replenishment_items:
        db_item = crud.create_replenishment_item(db, replenishment_item)
        items.append(db_item)
    return items

@api.get("/barcode", status_code=200)
async def get_barcode(barcode: schemas.Barcode):
    barcodeImage = bc.get('ean8', barcode.data, writer=ImageWriter())
    barcodeFile = BytesIO()
    barcodeImage.write(barcodeFile, writerOptions)
    barcodeFile.seek(0)
    return StreamingResponse(barcodeFile, media_type='image/png')
