import time, random
import redis
import json
pool = redis.ConnectionPool(host="172.17.0.5",port='6379')
r = redis.StrictRedis(connection_pool=pool)

r.delete('cf')
for i in range(1000000):
    ret = r.execute_command('bf.exists', 'cf', 'user%s'%i)

    r.execute_command('bf.add', 'cf', 'user%s'%i)
    
    if ret == 1:
        print(i)
        break
