import hashlib
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    VARCHAR,
    ForeignKey, Date, Index, Float, event, func,
)

from model.db import Base


class Thirteen_Pollution(Base):  # 2013年的污染物表
    __tablename__ = 'thirteen_pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    day = Column(Integer, nullable=False, comment='日期')
    hour = Column(Integer, nullable=False, comment='小时')
    city = Column(VARCHAR(40), nullable=False, comment='城市')  # 城市
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Thirteen_Information(Base):  # 2013年的信息表
    __tablename__ = 'thirteen_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    infor_id = Column(Integer, ForeignKey('thirteen_pollution.id'), comment='外键')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Fourteen_Pollution(Base):  # 2014年的污染物表
    __tablename__ = 'fourteen_pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city = Column(VARCHAR(40), nullable=False, comment='城市')  # 城市
    month = Column(Integer, nullable=False, comment='月份')
    day = Column(Integer, nullable=False, comment='日期')
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Fourteen_Information(Base):  # 2014年的信息表
    __tablename__ = 'fourteen_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    infor_id = Column(Integer, ForeignKey('fourteen_pollution.id'), comment='外键')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空



class Fifteen_Pollution(Base):  # 2015年的污染物表
    __tablename__ = 'fifteen_pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city = Column(VARCHAR(40), nullable=False, comment='城市')  # 城市
    month = Column(Integer, nullable=False, comment='月份')
    day = Column(Integer, nullable=False, comment='日期')
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Fifteen_Information(Base):  # 2015年的信息表
    __tablename__ = 'fifteen_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    infor_id = Column(Integer, ForeignKey('fifteen_pollution.id'), comment='外键')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空

class Sixteen_Pollution(Base):  # 2016年的污染物表
    __tablename__ = 'sixteen_pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city = Column(VARCHAR(40), nullable=False, comment='城市')  # 城市
    month = Column(Integer, nullable=False, comment='月份')
    day = Column(Integer, nullable=False, comment='日期')
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Sixteen_Information(Base):  # 2016年的信息表
    __tablename__ = 'sixteen_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    infor_id = Column(Integer, ForeignKey('sixteen_pollution.id'), comment='外键')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Seventeen_Information(Base):  # 2017年的污染物表
    __tablename__ = 'seventeen_pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city = Column(VARCHAR(40), nullable=False, comment='城市')  # 城市
    month = Column(Integer, nullable=False, comment='月份')
    day = Column(Integer, nullable=False, comment='日期')
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Seventeen_Pollution(Base):  # 2017年的信息表
    __tablename__ = 'seventeen_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    infor_id = Column(Integer, ForeignKey('seventeen_pollution.id'), comment='外键')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Eighteen_Pollution(Base):  # 2018年的污染物表
    __tablename__ = 'eighteen_pollution'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    city = Column(VARCHAR(40), nullable=False, comment='城市')  # 城市
    month = Column(Integer, nullable=False, comment='月份')
    day = Column(Integer, nullable=False, comment='日期')
    lon = Column(Float, nullable=False, comment='经度')
    lat = Column(Float, nullable=False, comment='维度')
    U = Column(Float, nullable=False, comment='水平风速')
    V = Column(Float, nullable=False, comment='垂直风速')
    TEMP = Column(Float, nullable=False, comment='温度')
    RH = Column(Float, nullable=False, comment='相对湿度')
    PSFC = Column(Float, nullable=False, comment='表面气压')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


class Eighteen_Information(Base):  # 2018年的信息表
    __tablename__ = 'eighteen_information'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    infor_id = Column(Integer, ForeignKey('eighteen_pollution.id'), comment='外键')
    PM2_5 = Column(Float, nullable=False, comment='PM2.5')
    PM10 = Column(Float, nullable=False, comment='PM10')
    SO2 = Column(Float, nullable=False, comment='SO2')
    NO2 = Column(Float, nullable=False, comment='NO2')
    CO = Column(Float, nullable=False, comment='CO')
    O3 = Column(Float, nullable=False, comment='O3')
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空