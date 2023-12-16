from pydantic import BaseModel
from datetime import date, datetime


class city_interface(BaseModel):
    name: str
    lon: float
    lat: float


class time_interface(BaseModel):
    Datetimes: datetime = None
    Dates: date = None


class pollution_interface(BaseModel):
    city_id: int
    time_id: int
    AQI: float
    predict_AQI: float = None
    main_pollution: int
    PM2_5: float
    PM10: float
    SO2: float
    NO2: float
    CO: float
    O3: float


class information_interface(BaseModel):
    U: float
    V: float
    TEMP: float
    RH: float
    PSFC: float
    pollution_id: int


class date_interface(BaseModel):
    year: int = None
    month: int = None
    day: int = None


class file_interface(BaseModel):
    size: int
    hash_md5: str
    hash_sha256: str
    name: str
    type: str


class event_interface(BaseModel):
    city_id: int
    begin_time_id: int
    end_time_id: int
    events: str

class events_interface(BaseModel):
    city: str
    begin_time: date
    end_time: date
    events: str

class hash_interface(BaseModel):
    size: int
    hash_md5: str
    hash_sha256: str
