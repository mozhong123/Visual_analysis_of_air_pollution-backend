from sqlalchemy import create_engine
from data import Thirteen_Information, Thirteen_Pollution, Fourteen_Information, Fourteen_Pollution, \
    Fifteen_Information, Fifteen_Pollution, Sixteen_Information, Sixteen_Pollution, Seventeen_Information, \
    Seventeen_Pollution, Eighteen_Information, Eighteen_Pollution
from const import SQLALCHEMY_DATABASE_URL

# 这里需要引入所有使用 Base 的 Model


create_table_list = [Thirteen_Pollution, Thirteen_Information, Fourteen_Pollution, Fourteen_Information,
                     Fifteen_Pollution,
                     Fifteen_Information, Sixteen_Pollution, Sixteen_Information, Seventeen_Pollution,
                     Seventeen_Information, Eighteen_Pollution, Eighteen_Information
                     ]

if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    for tb in create_table_list:
        tb.__table__.create(bind=engine, checkfirst=True)
