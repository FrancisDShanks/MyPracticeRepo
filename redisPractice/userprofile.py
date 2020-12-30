import random
from faker import Faker
import json


class UP(object):
    def __init__(self, uid, username, password, chinese_name, english_name, gender, position, email, phone, department):
        user = dict()
        user['uid'] = uid
        user['username'] = username
        user['password'] = password
        user['chinese_name'] = chinese_name
        user['english_name'] = english_name
        user['gender'] = gender
        user['position'] = position
        user['email'] = email
        user['phone'] = phone
        user['department'] = department
        self.user = user

    def __repr__(self):
        return self.get_json()

    def get_json(self):
        return json.dumps(self.user)

    def get_dict(self):
        return self.user

    def get_uid(self):
        return self.user['uid']



def create_faker_user(num=1):
    fc = Faker(locale='zh_CN')
    fe = Faker()
    users  = []
    
    for i in range(num):
        first_eng_name = fe.first_name()
        last_eng_name = fe.last_name()
        full_eng_name = ' '.join((first_eng_name, last_eng_name))
        email = '_'.join((first_eng_name, last_eng_name)) + '@test.com'
        password = '12345'
        gender = random.choice(('male', 'female'))
        dep = ['ISV', 'Test Centre', 'Admin', 'HR']

        user = UP(
        uid = i,
        username='_'.join((first_eng_name, last_eng_name)),
        password=password,
        chinese_name=fc.name(),
        english_name=full_eng_name,
        gender=gender,
        position=fc.job(),
        email=email,
        phone=fc.phone_number(),
        department=dep[random.randint(0,3)],
        )
        users.append(user)
    return users

if __name__ == "__main__":
    users = create_faker_user(10)
    for u in users:
        print(u)
            