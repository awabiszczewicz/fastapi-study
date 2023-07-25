from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}



#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "Favourite foods", "content": "Pizza", "id":2}]
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id: 
#             return p
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id: 
#             return i
