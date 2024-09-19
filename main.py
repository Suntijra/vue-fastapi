from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


# Define the allowed origins (e.g., frontend URLs)
origins = [
    "http://localhost:3030",  # Example: React app running on port 3030
    "http://localhost:3000"    # Example: React app running on port 3000
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

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Login(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(login: Login):
    user = login.username
    pwd = login.password
    if user == "dom" and pwd == "123":
        return {"msg": "good", "user": user}
    return {"error": "Invalid credentials", "msg": "bad"}



if __name__ == "__main__":
    
    uvicorn.run("main:app", host="127.0.0.1", port=3030, reload=True)