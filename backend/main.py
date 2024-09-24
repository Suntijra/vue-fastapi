from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openpyxl import Workbook
import os


# Define the allowed origins (e.g., frontend URLs)
origins = [
    "http://localhost:3030",  # Example: React app running on port 3030
    "http://localhost:3000" ,   # Example: React app running on port 3000,
    "http://localhost:5000" ,
    "http://localhost:80"  ,
    "http://localhost" 
]
app = FastAPI()
# Add CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from listed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the model for the User
class User(BaseModel):
    id: int
    name: str
    email: str

# In-memory "database"
users_db = []

# Home route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

class ExcelData(BaseModel):
    headers: list[str]
    headers_keys: list[str]
    rows: list[list]

@app.post("/export-excel")
def export_excel(data: ExcelData):
    # สร้าง Workbook และ Worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # เพิ่ม header ลงใน Excel
    ws.append(data.headers)

    # เพิ่ม rows ลงใน Excel
    for row in data.rows:
        ws.append(row)

    # กำหนดชื่อไฟล์ Excel ที่จะบันทึก
    file_name = "generated_data.xlsx"
    wb.save(file_name)

    # ส่งไฟล์ Excel กลับไปเป็น response
    return FileResponse(path=file_name, filename=file_name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=3030, reload=True)