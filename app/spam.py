from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import app.crud as crud
from redis import Redis

redis = Redis(host='redis', port=6379)

def report_spam(db: Session, msg: models.PrivateMessage):
        data = schemas.PrivateMessageFolderUpdate(id=msg.id, folder="spam")
        crud.update_message_folder(db, data)
        increment_spam_counter(msg)

def increment_spam_counter(msg: models.PrivateMessage):
    sender_key = get_spam_counter_redis_key(msg.from_userid)
    sender_dict_key = get_spam_user_dict(msg.from_userid)
    sender_dict = {k.decode(): int(v.decode()) for k, v in redis.hgetall(sender_dict_key).items()}
    if not redis.exists(sender_dict_key):
         sender_dict = {f'{msg.to_userid}': 1}
         redis.hmset(sender_dict_key, sender_dict)
         redis.incr(sender_key)
    elif sender_dict.get(f'{msg.to_userid}') is None:
         sender_dict[f'{msg.to_userid}'] = 1
         redis.hmset(sender_dict_key, sender_dict)
         redis.incr(sender_key)
    else:
         sender_dict[f'{msg.to_userid}'] += 1
         redis.hmset(sender_dict_key, sender_dict)

    redis.expire(sender_key, 604800) # 7 days in seconds

def un_spam(db: Session, msg: models.PrivateMessage):
    data = schemas.PrivateMessageFolderUpdate(id=msg.id, folder="inbox")
    crud.update_message_folder(db, data)
    decrement_spam_counter(msg)

def decrement_spam_counter(msg: models.PrivateMessage):
    sender_key = get_spam_counter_redis_key(msg.from_userid)
    sender_dict_key = get_spam_user_dict(msg.from_userid)
    sender_dict = {k.decode(): int(v.decode()) for k, v in redis.hgetall(sender_dict_key).items()}

    if redis.exists(sender_key) and redis.exists(sender_dict_key):
        if not (sender_dict.get(f'{msg.to_userid}') is None):
            sender_dict[f'{msg.to_userid}'] -= 1
            redis.hmset(sender_dict_key, sender_dict)
            if sender_dict[f'{msg.to_userid}'] == 0:
                sender_dict.pop(f'{msg.to_userid}')
                redis.decr(sender_key)
                redis.expire(sender_key, 604800)

def get_spam_counter_redis_key(from_uid: int) -> str:
    """Get the Redis key for a sender's spam count metric.

    Args:
        from_uid (int): The unique user ID of the sender.

    Returns:
        str: The key to use in Redis to read/write the spam counter.
    """
    return f'msg:spam-reports:uid:{from_uid}'

def get_spam_user_dict(from_uid: int) -> str:
    """Get the Redis key for a sender's spam dictionary metric.

    Args:
        from_uid (int): The unique user ID of the sender.

    Returns:
        str: The key to use in Redis to read/write the spam dict.
    """
    return f'msg:spam-reports-dict:uid:{from_uid}'