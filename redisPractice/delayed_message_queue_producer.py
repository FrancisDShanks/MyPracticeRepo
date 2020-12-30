import redis
import uuid
import json
import time
import faker
import random
from concurrent.futures import ProcessPoolExecutor
import multiprocessing, logging



def delay(msg, r):
    time.sleep(random.randint(1,3))
    value = json.dumps(msg)
    retry = time.time() + random.randint(1,10) # 设置不同的延时,retry表示处理这条数据的时间戳
    r.zadd("dq", {value: retry})


def producer(pid):
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    fk = faker.Faker()
    r1 = redis.StrictRedis(host='localhost', port=6379, db=0)
    for i in range(5):
        msg = {}
        msg['text'] = fk.paragraph()
        msg['name'] = fk.name()
        msg['id'] = str(uuid.uuid4())
        delay(msg, r1)
        logger.info('producer no.%s produced no.%s data.' % (pid, i))
    return 'subprocess No.' + str(pid) + ' done'


def main():
    futures = []
    with ProcessPoolExecutor(3) as executor:
        futures = [executor.submit(producer, i) for i in range(3)]
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info([f.result() for f in futures])
    logger.info('All Producers have Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    

    
    

if __name__ == "__main__":
    main()