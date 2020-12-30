#!/usr/bin/env python
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'FrancisD'

import time

class Funnel(object):
    def __init__(self, capacity, leaking_rate):
        self.capacity = capacity  # max space
        self.leaking_rate = leaking_rate  # quota/s
        self.left_quota = capacity  # left space
        self.leaking_ts = time.time()  # lastest leaking time

    def make_space(self):
        now_ts = time.time()
        delta_ts = now_ts - self.leaking_ts
        
        # water leaked in delta_ts time
        delta_quota = delta_ts * self.leaking_rate
        
        if delta_quota < 1:
            return
        self.left_quota += delta_quota
        self.leaking_ts = now_ts
        if self.left_quota > self.capacity:
            self.left_quota = self.capacity

    def watering(self, quota):
        self.make_space()
        if self.left_quota >= quota:
            self.left_quota -= quota
            return True
        return False


funnels = {}

def is_allowed(user_id, action_key, capacity, leaking_rate):
    key = f'{user_id}:{action_key}'
    funnel = funnels.get(key)
    if not  funnel:
        funnel = Funnel(capacity, leaking_rate)
        funnels[key] = funnel
    print(funnels)
    return funnel.watering(1)

for i in range(20):
    time.sleep(1)
    print(is_allowed('test','reply', 5, 0.5))
