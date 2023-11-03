from pydantic import BaseModel
from datetime import date,datetime
class city_interface(BaseModel):
    name: str
    lon: float
    lat: float


class time_interface(BaseModel):
    Datetimes : datetime = None
    Dates : date = None

class pollution_interface(BaseModel):
    city_id: int
    time_id:int
    AQI: float
    main_pollution : int
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
    pollution_id : int
