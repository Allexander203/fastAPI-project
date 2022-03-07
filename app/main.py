from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.functions import user
from . import models
from .database import engine
from .routers import post, user, auth, vote
from.config import settings

# obsolete, because of alimbic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # кои домейни могат да изпрщат заявки към API ти

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)  # imports the rout from post.py
app.include_router(user.router)  # imports the rout from user.py
app.include_router(auth.router)  # imports the rout from auth.py
app.include_router(vote.router)  # imports the rout from vote.py


@app.get("/")
def root():
    return {"Message": "Hello world successfully deployed from ci/cd pipeline"}
