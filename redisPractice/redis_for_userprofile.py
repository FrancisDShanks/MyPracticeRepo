import redis
from userprofile import create_faker_user
import json


def op1_save_to_redis(r, users):
    for u in users:
        r.set('user:%s' % u.get_uid(), u.get_dict())
        r.sadd('users', u.get_uid())
    return True

def op1_load_from_redis(r):
    users = []
    for uid in r.smembers('users'):
        raw = r.get("user:{0}".format(uid.decode()))
        users.append(json.loads(raw))
    return users


def main():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, max_connections=10)
    redis1 = redis.StrictRedis(connection_pool=pool)

    users = create_faker_user(10)
    loadusers = []
    try:
        op1_save_to_redis(redis1, users)
    except Exception as e:
        print(e)
    else:
        print("Done save option1")

    try:
        loadusers = op1_load_from_redis(redis1)
    except Exception as e:
        print(e)
    else:
        print("Done load option1")

    print(users)
    print(loadusers)

if __name__ == "__main__":
    main()