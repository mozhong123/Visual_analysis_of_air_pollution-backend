from fastapi.encoders import jsonable_encoder
from model.data import City, Time, Pollution, Information
from model.db import dbSession
from type.data import city_interface, time_interface, pollution_interface, information_interface


class PollutionModel(dbSession):
    def add_data(self, obj: pollution_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Pollution(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id


class InformationModel(dbSession):
    def add_data(self, obj: information_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Information(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id


class CityModel(dbSession):
    def add_city(self, obj: city_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = City(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_city_id_by_city_name(self, city_name: str):
        with self.get_db() as session:
            id = session.query(City.id).filter(City.name == city_name).first()
            session.commit()
            return id


class TimeModel(dbSession):
    def add_time(self, obj: time_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Time(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id
