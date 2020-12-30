import redis
import uuid
import json
import time
import faker
import random
from concurrent.futures import ProcessPoolExecutor
import multiprocessing, logging

def loop(r, cid):
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    
    # while True:
    cnt = 0
    while cnt < 20:
        values = r.zrangebyscore("dq", 0, time.time(), start=0, num=1) # 根据当前时间戳判断是否处理
        if not values:
            time.sleep(1) # 队列没有需要处理的,休眠1s
            continue
        value = values[0]
        success = r.zrem("dq", value) # 从队列里面移除要处理的
        if success: # 这里可能有多个consumer都找到了values,但是只能有一个zrem成功,最终只会有一个consumer处理
            msg = json.loads(value)
            logger.info("cosumer no.%s is dealing message..." % cid)
            logger.info(msg)
        cnt += 1


def consumer(cid):
    r1 = redis.StrictRedis(host='localhost', port=6379, db=0)
    loop(r1, cid)
    return 'consumer no%s is done!!!' % cid


def main():
    futures = []
    with ProcessPoolExecutor(2) as executor:
        futures = [executor.submit(consumer, i) for i in range(2)]
    
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info([c.result() for c in futures])
    logger.info('All Comsumers have done !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    
    

if __name__ == "__main__":
    main()