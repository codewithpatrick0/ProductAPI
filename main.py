from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, notes

app = FastAPI()
app.include_router(auth.router_api)
app.include_router(notes.router_api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}
