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


class Information(Base):
    __tablename__ = 'information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    pollution_id = Column(Integer, ForeignKey('pollution.id'), comment='外键')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False, comment='城市')  # 城市
    begin_time_id = Column(Integer, ForeignKey('time.id'), nullable=False, comment='起始时间')
    end_time_id = Column(Integer, ForeignKey('time.id'), nullable=False, comment='终止时间')
    events = Column(VARCHAR(512), nullable=False)


class File(Base):  # 文件表
    __tablename__ = 'file'
    __table_args__ = (
        Index('ix_file_has_delete_size_hash',  "size", "hash_md5", "hash_sha256"),  # 非唯一的索引
    )
    id = Column(Integer, primary_key=True)  # 文件 id
    size = Column(Integer, nullable=False)  # 文件大小（字节）
    hash_md5 = Column(VARCHAR(128), nullable=False)  # 文件哈希md5
    hash_sha256 = Column(VARCHAR(128), nullable=False)  # 文件哈希sha256
    name = Column(VARCHAR(128), nullable=True)  # 文件名
    type = Column(VARCHAR(128), nullable=True)  # 文件类型
    create_dt = Column(DateTime,default=func.now(), nullable=False)  # 文件创建时间