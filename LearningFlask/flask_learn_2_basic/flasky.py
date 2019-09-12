import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# intial database migration
# run 'flask db init' in terminal to initial the function
migrate = Migrate(app, db)

# build shell context to auto import db,User and Role when run 'flask shell'
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
