from sqlalchemy import create_engine
from data import Information, Pollution, City, Time, Event, File, Gpt
from const import SQLALCHEMY_DATABASE_URL

# 这里需要引入所有使用 Base 的 Model


create_table_list = [City,Time,Pollution,Information,Event,File,Gpt
                     ]

if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    for tb in create_table_list:
        tb.__table__.create(bind=engine, checkfirst=True)
