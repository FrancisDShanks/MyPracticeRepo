from concurrent.futures import ProcessPoolExecutor
import random, os, time
from multiprocessing import Manager, log_to_stderr
import logging
from redis import StrictRedis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DEFAULT_DB = 0 

def pro(n, r=StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DEFAULT_DB)):
    logger = log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.warning('producer no.%s start' % n)
    for i in range(3):
        time.sleep(random.randint(1,3))
        logger.warning('producer no.%s produced no.%s' % (n, i))
        r.rpush('goods', '[%s, %s]' % (n, i))
    logger.warning('producer no.%s done' % n)
    return 'producer no.%s done' % n

def con(n, r=StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DEFAULT_DB)):
    logger = log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.warning('Consumer no.%s start' % n)
    for i in range(5):
        time.sleep(random.randint(2,3))
        v = r.blpop('goods')
        logger.warning('consumer no.%s consume no.%s, value is %s' % (n, i, v))
    logger.warning('consumer no.%s done' % n)
    return 'consumer no.%s done' % n
        

def main():
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(pro, i) for i in range(5)]
        futuress = [executor.submit(con, i) for i in range(5)]

    # for f in futures:
    #     print(f.result())
    #for f in futuress:
    #    print(f.result())

if __name__ == '__main__':
    main()
    # redis_conn = StrictRedis(host='localhost', port=6379, db=0)
    # print(redis_conn)
    # redis_conn.rpush('goods','1,2')

