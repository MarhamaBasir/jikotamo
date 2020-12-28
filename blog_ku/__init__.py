from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app=Flask(__name__)
app.config['SECRET_KEY']='5459064d17cbb76504a0c7cbcf343704'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///web.db'
app.config['CKEDITOR_WEIGHT'] = 400

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)

login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_view='login_admin'
login_manager.login_message_category = 'info'

from blog_ku import routes