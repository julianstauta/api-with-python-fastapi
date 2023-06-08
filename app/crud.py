from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

MAX_PER_PAGE = 10

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_msg_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PrivateMessage).offset(skip).limit(limit).all()

def create_message(db: Session, private_message: schemas.PrivateMessageCreate):
    db_msg = models.PrivateMessage(from_userid = private_message.from_userid, 
                                    to_userid = private_message.to_userid,
                                    subject = private_message.subject,
                                    message = private_message.message)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

def update_message_folder(db: Session, msg: schemas.PrivateMessageFolderUpdate):
    db_msg = db.query(models.PrivateMessage).where(models.PrivateMessage.id == msg.id).first()
    db_msg.folder = msg.folder
    db.commit()
    db.refresh(db_msg)
    return db_msg

def update_messages(db: Session, data:schemas.PrivateMessageUpdate):
    message_ids = data.message_id_list
    if not message_ids:
        raise HTTPException(status_code=422, detail='Please provide message IDs.')
    elif not isinstance(message_ids, list):
        raise HTTPException(status_code=422, detail='Please provide a list of message IDs.')
    elif len(message_ids) > MAX_PER_PAGE:
        raise HTTPException(status_code=422, detail='Requested too many messages.')
    message_ids = [str(ids) for ids in message_ids]
    read = _get_and_validate_optional_boolean(data.read)
    trash = _get_and_validate_optional_boolean(data.trash)
    spam = _get_and_validate_optional_boolean(data.spam)

    set_folder_to = "read" if read else "trash" if trash else "spam" if spam else "inbox" 

    db.query(models.PrivateMessage).filter(models.PrivateMessage.id.in_(message_ids)).update({'folder': set_folder_to})
    db.commit()

                                    
def _get_and_validate_optional_boolean(value):
    if value in (None, True, False):
        return value
    elif value == 'true':
        return True
    elif value == 'false':
        return False
    raise HTTPException(status_code=422, detail='Invalid option: {}'.format(value))                          