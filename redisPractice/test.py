
from concurrent.futures import ProcessPoolExecutor
import multiprocessing, logging
import random, time
from multiprocessing import Manager, Lock
import asyncio
ret = []

async def fn1():
    asyncio.sleep(random.randint(1,2))
    n = random.randint(1,9)
    print(n)



def fn2(res):
    global ret
    res = res.result()
    print(res)
    ret.append(res * 10)

def main():
    loop = asyncio.get_event_loop()
    for i in range(5):
        loop.run_until_complete(fn1)
    
if __name__ == "__main__":
    main()