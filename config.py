class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:///configs/cache.sqlite3"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Строчка ниже не хочет работать без ошибок, пришлось записать две верхние (из интернета)
    # app.config["SQLAlchemy_DATABASE_URI"] = "sqlite:///sqlite3.db"
    JSON_AS_ASCII = False
