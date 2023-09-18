from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
import pathlib


# Зчитуємо дані з конфігураційного файлу config.ini
file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = 'sqlite'
password = '567234'
db_name = 'hw07'
domain = 'localhost'

# Формуємо URL для підключення до бази даних SQLite
url = f'sqlite:///{db_name}.db'

# Ініціалізуємо об'єкт для роботи з базою даних
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)

# Створюємо сеанс для взаємодії з базою даних
DBSession = sessionmaker(bind=engine)
session = DBSession()
