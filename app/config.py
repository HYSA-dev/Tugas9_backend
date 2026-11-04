import os

class Config:
    # Ganti 'root' dan password MySQL kamu jika ada
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql_99007@localhost/db_uts_backend'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'uts-backend-stikom'