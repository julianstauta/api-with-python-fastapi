from fastapi import Depends, FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

import redis

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
cache = redis.Redis(host='redis', port=6379)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", dependencies=[Depends(jwtBearer())], response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", dependencies=[Depends(jwtBearer())], response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/msg/list/", dependencies=[Depends(jwtBearer())], response_model=list[schemas.PrivateMessage])
def get_message_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    msg_list = crud.get_msg_list(db, skip=skip, limit=limit)
    return msg_list

@app.post("/msg/create/", dependencies=[Depends(jwtBearer())], response_model=schemas.PrivateMessage)
def create_message(msg: schemas.PrivateMessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, private_message=msg)

@app.put("/msg/list/")
def put_update(data: schemas.PrivateMessageUpdate, db: Session = Depends(get_db)):
    crud.update_messages(db=db, data=data)
    return {"msg": "Success"}

@app.post("/users/login")
def user_login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email = user.email
    pword = user.password
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exists")
    if db_user.hashed_password == pword + "notreallyhashed":
        print("loged in !!!!")
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=400, detail="User and password does't match")
