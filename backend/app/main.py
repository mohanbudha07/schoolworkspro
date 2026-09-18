from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .seed import seed
from .routers import auth, admin, academic

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="SchoolWorksPro", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(academic.router)


@app.get("/api/health")
def health():
    return {"ok": True, "product": "SchoolWorksPro"}
