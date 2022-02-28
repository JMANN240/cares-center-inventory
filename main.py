from io import BytesIO
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import barcode as bc
from barcode.writer import ImageWriter
from typing import Optional
import crud
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session


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

@api.get("/donors", response_model=list[schemas.Donor])
def read_donors(db: Session = Depends(get_db)):
    donors = crud.get_donors(db)
    return donors

@api.post("/donors", response_model=schemas.Donor)
def create_donor(donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    return crud.create_donor(db, donor=donor)

@api.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)

@api.delete("/items")
def delete_items(db: Session = Depends(get_db)):
    crud.delete_items(db)
    return 200

@api.get("/barcode", status_code=200)
async def get_barcode(barcode: schemas.Barcode):
    barcodeImage = bc.get('ean8', barcode.data, writer=ImageWriter())
    barcodeFile = BytesIO()
    barcodeImage.write(barcodeFile, writerOptions)
    barcodeFile.seek(0)
    return StreamingResponse(barcodeFile, media_type='image/png')