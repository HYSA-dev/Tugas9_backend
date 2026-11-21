import os


class Config:
    # Ganti 'root' dan password MySQL kamu jika ada
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:mysql_99007@localhost/db_uts_backend"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "uts-backend-stikom"


    # Konfigurasi NoSQL MongoDB (Pertemuan 9)
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "db_backend_logs")
