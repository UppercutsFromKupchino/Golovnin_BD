class Config:
    dialect = 'postgresql'
    username = 'postgres'
    password = 'alp37327'
    host = 'localhost'
    db_name = 'Golovnin_BD'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-bountyhunter'
