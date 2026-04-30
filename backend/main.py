from fastapi import FastAPI
from routers import teachers, pupils # import both 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API School")

# Connexion with the routers
app.include_router(teachers.router)
app.include_router(pupils.router)

#to connect the frontend to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Just a simple home route to check if the API is running
@app.get("/")
def home():
    return {"message": "Welcome to the API of the school !"}