from io import BytesIO
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, StreamingResponse, RedirectResponse
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
from typing import Optional

# Setup

def proper(text):
    return " ".join([word[0].upper() + word[1:] for word in text.split(" ")])

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
templates.env.filters['proper'] = proper

writerOptions = {
    'module_width': 0.8,
    'module_height': 16,
    'text_distance': 2.0,
    'quiet_zone': 2.0,
    'background': '#ffffff',
    'foreground': '#000000',
    'font_size': 30,
}

# Authentication

def check_auth(db, manager_id):
    if manager_id is None:
        return False
    
    manager = crud.get_manager_by_id(db, manager_id)
    return manager.is_active

def check_admin(db, manager_id):
    if manager_id is None:
        return False
    
    manager = crud.get_manager_by_id(db, manager_id)
    return manager.is_admin

# Front-end stuff

@app.get("/")
async def index_page(request: Request, manager_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)):
    if not check_auth(db, manager_id):
        return RedirectResponse(f"/login")
    manager = crud.get_manager_by_id(db, manager_id)
    return templates.TemplateResponse("index.html", {"request": request, "manager": manager})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/items")
async def items_page(request: Request, manager_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)):
    if not check_auth(db, manager_id):
        return RedirectResponse(f"/login")
    return templates.TemplateResponse("items.html", {"request": request, 'table': 'items'})

@app.get("/transaction")
async def transaction_page(request: Request, manager_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)):
    if not check_auth(db, manager_id):
        return RedirectResponse(f"/login")
    return templates.TemplateResponse("transaction.html", {"request": request})

@app.get("/transactions")
async def transactions_page(request: Request, manager_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)):
    if not check_auth(db, manager_id):
        return RedirectResponse(f"/login")
    return templates.TemplateResponse("transactions.html", {"request": request})

@app.get("/managers")
async def managers_page(request: Request, manager_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)):
    if not (check_auth(db, manager_id) and check_admin(db, manager_id)):
        return RedirectResponse(f"/login")
    return templates.TemplateResponse("managers.html", {"request": request, 'table': 'managers'})

@app.get("/donors")
async def donors_page(request: Request, manager_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)):
    if not check_auth(db, manager_id):
        return RedirectResponse(f"/login")
    return templates.TemplateResponse("donors.html", {"request": request, 'table': 'donors'})



# Back-end

@api.post("/login")
def login(login: schemas.Login, response: Response, db: Session = Depends(get_db)):
    try:
        db_manager = crud.get_manager_by_username(db, login.username)
        is_password_correct = pbkdf2_sha256.verify(login.password, db_manager.passhash)
        is_active = db_manager.is_active
    
        if is_password_correct and is_active:
            response.set_cookie(key="manager_id", value=db_manager.id, max_age=60*60*6)
            response.status_code = 200
            return response
        else:
            if not is_password_correct:
                response.body = b"Incorrect password"
            elif not is_active:
                response.body = b"Inactive account"
            response.status_code = 406
            return response
    except sqlalchemy.exc.NoResultFound:
        response.body = b'Username not found'
        response.status_code = 406
        return response

@api.post("/logout")
def logout(response: Response):
    response.set_cookie(key="manager_id", value=None, max_age=0)
    response.status_code = 200
    return response



@api.post("/managers", response_model=schemas.ManagerRead)
def create_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db)):
    return crud.create_manager(db, manager)

@api.get("/managers", response_model=List[schemas.ManagerRead])
def read_managers(db: Session = Depends(get_db)):
    return crud.get_managers(db)

@api.get("/managers/id/{id}", response_model=schemas.ManagerRead)
def read_manager_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_manager_by_id(db, id)

@api.put("/managers", response_model=schemas.Manager)
def update_manager(manager: schemas.Manager, db: Session = Depends(get_db)):
    crud.update_manager(db, manager)
    return manager



@api.post("/donors", response_model=schemas.DonorRead)
def create_donor(donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    return crud.create_donor(db, donor)@api.get("/donors", response_model=List[schemas.Donor])

@api.get("/donors", response_model=List[schemas.DonorRead])
def read_donors(db: Session = Depends(get_db)):
    return crud.get_donors(db)

@api.get("/donors/id/{id}", response_model=schemas.DonorRead)
def read_donor_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_donor_by_id(db, id)

@api.put("/donors", response_model=schemas.Donor)
def update_donor(donor: schemas.Donor, db: Session = Depends(get_db)):
    crud.update_donor(db, donor)
    return donor



@api.post("/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@api.get("/items", response_model=List[schemas.ItemRead])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@api.get("/items/id/{id}", response_model=schemas.ItemRead)
def read_item_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_item_by_id(db, id)

@api.get("/items/barcode/{barcode}", response_model=schemas.ItemRead)
def read_item_by_barcode(barcode: str, db: Session = Depends(get_db)):
    return crud.get_item_by_barcode(db, barcode)

@api.put("/items", response_model=schemas.Item)
def update_item(item: schemas.Item, db: Session = Depends(get_db)):
    crud.update_item(db, item)
    return item



@api.post("/transactions", response_model=schemas.TransactionRead)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

@api.get("/transactions", response_model=List[schemas.TransactionRead])
def read_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)

@api.get("/transactions/id/{id}", response_model=schemas.TransactionRead)
def read_transactions_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_transaction_by_id(db, id)



@api.post("/transactions/item", response_model=schemas.TransactionItemRead)
def create_transaction_item(transaction_item: schemas.TransactionItemCreate, db: Session = Depends(get_db)):
    crud.update_item_quantity_by_id_relative(db, transaction_item.item_id, -transaction_item.quantity)
    return crud.create_transaction_item(db, transaction_item)

@api.get("/transactions/id/{id}/items", response_model=List[schemas.TransactionItemRead])
def get_transaction_items_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_transaction_items_by_transaction_id(db, id)



@api.post("/transactions/weight", response_model=schemas.DonorWeightRead)
def create_transaction_donor_weight(donor_weight: schemas.DonorWeightCreate, db: Session = Depends(get_db)):
    return crud.create_donor_weight(db, donor_weight)

@api.get("/transactions/id/{id}/weights", response_model=List[schemas.DonorWeightRead])
def get_transaction_weights_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_donor_weights_by_transaction_id(db, id)



@api.get("/barcode", status_code=200)
async def get_barcode_image(data: str):
    barcodeImage = bc.get('ean8', data, writer=ImageWriter())
    barcodeFile = BytesIO()
    barcodeImage.write(barcodeFile, writerOptions)
    barcodeFile.seek(0)
    return StreamingResponse(barcodeFile, media_type='image/png')
