# flask_learn_1_basic
## Practice based on book **_Flask Web Development_** Chapter 5-7
## using package:
* flask
* flask-moment
* flask-wtf
* flask-script
* flask-bootstrap
* flask-sqlalchemy
* flask-migrate
* flask-mail

## data base migrate command
First, migrate changes. (We can use this command to create tables if it is the first run)
```
flask db migrate -m "some comment"
```
Then,**check the migrate script generated carefully**. 

After that, run below command to update the database.
```
flask db upgrade
```