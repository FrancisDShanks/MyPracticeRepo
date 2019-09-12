from hello import Role, User
from hello import db
db.drop_all()
db.create_all()

admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')

user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)

db.session.add(admin_role)
db.session.add(mod_role)
db.session.add(user_role)
db.session.add(user_john)
db.session.add(user_susan)
db.session.add(user_david)

db.session.commit()

print(admin_role.id)
print(mod_role.id)
print(user_role.users)

admin_role.name = 'Administrator'
db.session.add(admin_role)
db.session.commit()

print(admin_role)

db.session.delete(mod_role)
db.session.commit()

print(Role.query.all())
print(User.query.all())
print(str(User.query.filter_by(role=user_role)))