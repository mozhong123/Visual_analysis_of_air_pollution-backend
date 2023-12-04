import hashlib
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    VARCHAR,
    ForeignKey, Date, Index, Float, event, func,
)

from model.db import Base


class City(Base):  # 城市表
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    name = Column(VARCHAR(40), nullable=False, unique=True, comment='城市')  # 城市
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')


class Time(Base):  # 时间表
    __tablename__ = 'time'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    Datetimes = Column(DateTime, nullable=True,unique=True)
    Dates = Column(Date, nullable=True,unique=True)


class Pollution(Base):
    __tablename__ = 'pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False, comment='城市')  # 城市
    time_id = Column(Integer, ForeignKey('time.id'), nullable=False, comment='时间')
    main_pollution = Column(Integer,  nullable=False)
    AQI = Column(Float, nullable=False, comment='AQI')
    predict_AQI = Column(Float, nullable=True, comment='AQI')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')


class Information(Base):  # 2013年的信息表
    __tablename__ = 'information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    pollution_id = Column(Integer, ForeignKey('pollution.id'), comment='外键')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
