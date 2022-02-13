class Config:
    dialect = 'postgresql'
    username = 'luqubhcondwbtk'
    password = 'ca410cc9828a8f4d40e711ac20f40df1e7463e1db66b12c84673a562a6dd3893'
    host = 'ec2-54-76-249-45.eu-west-1.compute.amazonaws.com'
    db_name = 'd1cq3sm6rep74o'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-bountyhunter'
