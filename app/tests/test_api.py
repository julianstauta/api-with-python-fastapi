from fastapi.testclient import TestClient
from ..main import app, crud, models, schemas
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
import pytest
from app import spam

client = TestClient(app)
models.Base.metadata.create_all(bind=engine)

from redis import Redis
redis = Redis(host='redis', port=6379)

@pytest.fixture(name="session")  # 
def session_fixture():  # 
    models.Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session  # 

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_messages_put_mark_read_and_deleted(session:Session):
    # setup
    def get_session_override():
        return session 

    user_1 = create_new_user(session, "test1@test.com", "x")
    user_2 = create_new_user(session, "test2@test.com", "x")

    msg_1 = create_message(session, user_1.id, user_2.id)
    msg_2 = create_message(session, user_1.id, user_2.id)

    # exercise
    data={
        "message_id_list": [
            msg_1.id, msg_2.id
        ],
        "read": "true",
        "trash": "true",
    }
    response = client.put(
        "/msg/list/",
        json=data,
    )

    # verify
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}
    
    session.refresh(msg_1)
    assert msg_1.folder == "trash"
    assert msg_1.unread == "N"

    session.refresh(msg_2)
    assert msg_2.folder == "trash"
    assert msg_2.unread == "N"

    # teardown
    session.query(models.PrivateMessage).filter(models.PrivateMessage.id==msg_1.id).delete()
    session.query(models.PrivateMessage).filter(models.PrivateMessage.id==msg_2.id).delete()


def create_message(db: Session, from_uid: int, to_uid: int, subject: str = "test", message: str = "blank") -> models.PrivateMessage:
    new_msg = schemas.PrivateMessageCreate(
        from_userid = from_uid,
        to_userid = to_uid,
        subject = subject,
        message = message,)
    
    return crud.create_message(db, new_msg)


def create_new_user(db: Session, email: str, p: str) -> models.User:
    db_user = crud.get_user_by_email(db, email)
    if db_user:
        return db_user
    
    new_user = schemas.UserCreate(email = email, password = p)
    return crud.create_user(db=db, user=new_user)

def test_report_spam_one_user(session:Session):
    # setup
    def get_session_override():
        return session 

    user_1 = create_new_user(session, "test1@test.com", "x")
    user_2 = create_new_user(session, "test2@test.com", "x")
    msg_1 = create_message(session, user_2.id, user_1.id)
    msg_2 = create_message(session, user_2.id, user_1.id)
    msg_3 = create_message(session, user_2.id, user_1.id)

    sender_key = spam.get_spam_counter_redis_key(msg_1.from_userid)
    sender_dict_key = spam.get_spam_user_dict(msg_1.from_userid)
    initial_count = 0
    redis.set(sender_key, initial_count)
    redis.delete(sender_dict_key)
  
    spam.report_spam(session, msg_1)
    spam.report_spam(session, msg_2)
    spam.report_spam(session, msg_3)
    session.refresh(msg_1)
    session.refresh(msg_2)
    session.refresh(msg_3)

    assert msg_1.folder == "spam"
    assert msg_2.folder == "spam"
    assert msg_3.folder == "spam"

    after_count = int(redis.get(sender_key))
    assert after_count == initial_count + 1

    # teardown
    session.query(models.PrivateMessage).filter(models.PrivateMessage.id==msg_1.id).delete()

def test_report_spam_2_users(session:Session):
    # setup
    def get_session_override():
        return session 

    user_1 = create_new_user(session, "test1@test.com", "x")
    user_2 = create_new_user(session, "test2@test.com", "x")
    user_3 = create_new_user(session, "test3@test.com", "x")
    msg_1 = create_message(session, user_2.id, user_1.id)
    msg_2 = create_message(session, user_2.id, user_1.id)
    msg_3 = create_message(session, user_2.id, user_3.id)

    sender_key = spam.get_spam_counter_redis_key(msg_1.from_userid)
    sender_dict_key = spam.get_spam_user_dict(msg_1.from_userid)
    initial_count = 0
    redis.set(sender_key, initial_count)
    redis.delete(sender_dict_key)
  
    spam.report_spam(session, msg_1)
    spam.report_spam(session, msg_2)
    spam.report_spam(session, msg_3)
    session.refresh(msg_1)

    assert msg_1.folder == "spam"
    assert msg_2.folder == "spam"
    assert msg_3.folder == "spam"

    after_count = int(redis.get(sender_key))
    assert after_count == initial_count + 2

    # teardown
    session.query(models.PrivateMessage).filter(models.PrivateMessage.id==msg_1.id).delete()
    sender_dict_key = spam.get_spam_user_dict(msg_1.from_userid)
    redis.delete(sender_key)
    redis.delete(sender_dict_key)
    
def test_report_un_spam_one_user(session:Session):
    # setup
    def get_session_override():
        return session 

    user_1 = create_new_user(session, "test1@test.com", "x")
    user_2 = create_new_user(session, "test2@test.com", "x")
    msg_1 = create_message(session, user_2.id, user_1.id)
    msg_2 = create_message(session, user_2.id, user_1.id)
    msg_3 = create_message(session, user_2.id, user_1.id)

    sender_key = spam.get_spam_counter_redis_key(msg_1.from_userid)
    sender_dict_key = spam.get_spam_user_dict(msg_1.from_userid)
    initial_count = 0
    redis.set(sender_key, initial_count)
    redis.delete(sender_dict_key)
  
    spam.report_spam(session, msg_1)
    spam.report_spam(session, msg_2)
    spam.report_spam(session, msg_3)
    session.refresh(msg_1)
    session.refresh(msg_2)
    session.refresh(msg_3)


    assert msg_1.folder == "spam"
    assert msg_2.folder == "spam"
    assert msg_3.folder == "spam"

    spam.un_spam(session, msg_1)
    spam.un_spam(session, msg_2)
    spam.un_spam(session, msg_3)

    assert msg_1.folder == "inbox"

    after_count = int(redis.get(sender_key))
    assert after_count == initial_count

    # teardown
    session.query(models.PrivateMessage).filter(models.PrivateMessage.id==msg_1.id).delete()


    