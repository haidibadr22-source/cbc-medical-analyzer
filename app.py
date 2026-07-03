from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from graph import process_report

import tempfile
import shutil
import os

app = FastAPI(title="CBC Medical Analyzer")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return JSONResponse(
            {"error": "Please upload a PDF."},
            status_code=400
        )

    temp_dir = tempfile.mkdtemp()

    pdf_path = os.path.join(temp_dir, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        result = process_report(pdf_path)

        return result

    finally:

        try:
            os.remove(pdf_path)
            os.rmdir(temp_dir)
        except:
            pass
