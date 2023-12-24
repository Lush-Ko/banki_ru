import io
import os

import fastapi.exceptions
import pandas as pd
import yaml
from fastapi import FastAPI, Depends, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from application.backend.database import get_db, engine
from application.backend.reviews import router as reviews_rooter
from fit_predict import main as fit_predict_main
from predict import main as predict_main

app = FastAPI(title="banki_ru_system",
              version="0.0.1")

app.include_router(reviews_rooter.router)

path_to_static = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static",
          StaticFiles(directory="./templates/static"),
          name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определение модели SQLAlchemy
Base = declarative_base()

# Инициализация Jinja2 для работы с HTML-шаблонами
templates = Jinja2Templates(directory="templates")


# API endpoint для отображения HTML
@app.get("/", response_class=HTMLResponse)
async def get_analytics_dashboard(request: Request,
                                  db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "predicter_home.html",
        {"request": request})


@app.get("/home", name='home', response_class=HTMLResponse)
async def get_analytics_dashboard(request: Request,
                                  db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "predicter_home.html",
        {"request": request})


@app.get("/predicter_home", name='predicter_home', response_class=HTMLResponse)
async def get_predicter(request: Request,
                        db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "predicter_home.html",
        {"request": request})


@app.get("/about", name='about', response_class=HTMLResponse)
async def get_about(request: Request,
                    db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "about.html",
        {"request": request})


@app.get("/predicter_home")
async def get_about(request: Request,
                    db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "predicter_home.html",
        {"request": request})


@app.get("/predicter_home/results")
async def get_about(request: Request,
                    db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "predicter_home_results.html",
        {"request": request})
@app.get("/predicter_home_predict")
async def get_about(request: Request,
                    db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "predicter_home_predict.html",
        {"request": request})

@app.post("/predicter_home/results")
async def fit_predict(file: UploadFile):
    content = await file.read()
    # Process the file using Pandas or any other library
    df = pd.read_csv(io.BytesIO(content))

    # Store the data in PostgreSQL
    with open("data/config.yaml", "r", encoding='utf-8') as stream:
        args = yaml.safe_load(stream)['config_data']
    df.to_csv(args['config_data']['preproc_file_path'], index=False)
    fit_predict_main()
    return {"filename": file.filename, "content_type": file.content_type}


@app.post("/predicter_home/predict")
async def predict(file: UploadFile):
    content = await file.read()
    with open("uploaded_file.csv", "wb") as f:
        f.write(content)
    # Process the file using Pandas or any other library
    df = pd.read_csv(io.BytesIO(content))
    # Store the data in PostgreSQL
    with open("data/config.yaml", "r", encoding='utf-8') as stream:
        args = yaml.safe_load(stream)['config_data']
    df.to_csv(args['config_data']['preproc_file_path'], index=False)
    predict_main()
    return {"filename": file.filename, "content_type": file.content_type}
