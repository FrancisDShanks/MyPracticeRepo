import redis
import time

pool = redis.ConnectionPool(max_connections=2, host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)

def is_action_allowed(user_id, action_key, period, max_cnt):
    "do an action if allowed based on args and return True or return False"
    #key = 'hist:%s:%s' % (user_id, action_key)
    key = user_id
    now_ts = int(time.time() * 1000)
    with r.pipeline() as pipe:       

        # remove the records before the slicing window
        # the window is (now_ts - period*1000, now_ts]
        # the range to be removed is [0, now_ts - period*1000]
        pipe.zremrangebyscore(key, 0, now_ts - period*1000)

        pipe.zcard(key)
        # set expire time, give one more second
        pipe.expire(key, period + 1)

        _,current_cnt,_ = pipe.execute()
        
    
    if current_cnt <= max_cnt:
        r.zadd(key, {now_ts: now_ts})
        return True
    return False
    

for i in range(20):
    print(is_action_allowed("test", "reply", 10, 3))
    time.sleep(1)