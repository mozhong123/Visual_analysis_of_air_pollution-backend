import random
from datetime import datetime, date

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, extract, between, desc, asc
from sqlalchemy.orm import aliased

from model.data import City, Time, Pollution, Information, File, Event, Gpt
from model.db import dbSession
from type.data import city_interface, time_interface, pollution_interface, information_interface, file_interface, \
    event_interface, hash_interface, gpt_interface


class PollutionModel(dbSession):
    def add_data(self, obj: pollution_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Pollution(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_pollution_by_city_date(self, city, time, type):
        with self.get_db() as session:
            query = session.query(Pollution.AQI, Pollution.PM2_5, Pollution.PM10, Pollution.SO2, Pollution.NO2,
                                  Pollution.CO, Pollution.O3
                                  ).outerjoin(City, City.id == Pollution.city_id).outerjoin(Time,
                                                                                            Time.id == Pollution.time_id)
            if type == 0:
                pollutions = query.filter(
                    Time.Dates == time, City.name == city
                ).first()
            else:
                pollutions = query.filter(
                    Time.Datetimes == time, City.name == city
                ).first()
            session.commit()
            return pollutions

    def get_pollution_by_date(self, time, type):
        with self.get_db() as session:
            query = session.query(Pollution.AQI, Pollution.PM2_5, Pollution.PM10, Pollution.SO2, Pollution.NO2,
                                  Pollution.CO, Pollution.O3, City.name, City.lon, City.lat
                                  ).outerjoin(City, City.id == Pollution.city_id).outerjoin(Time,
                                                                                            Time.id == Pollution.time_id)
            if type == 0:
                pollutions = query.filter(
                    Time.Dates == time
                ).all()
            else:
                pollutions = query.filter(
                    Time.Datetimes == time
                ).all()
            session.commit()
            return pollutions

    def get_rank_by_date(self, time, type):
        with self.get_db() as session:
            query = session.query(Pollution.AQI, City.name
                                  ).outerjoin(City, City.id == Pollution.city_id).outerjoin(Time,
                                                                                            Time.id == Pollution.time_id)
            if type == 0:
                pollutions = query.filter(
                    Time.Dates == time
                ).order_by(asc(Pollution.AQI)).limit(10).all()
            else:
                pollutions = query.filter(
                    Time.Datetimes == time
                ).order_by(asc(Pollution.AQI)).limit(10).all()
            session.commit()
            return pollutions

    def get_two_aqi_by_year_city(self, year, city):
        with self.get_db() as session:
            aqis = session.query(Pollution.AQI, Pollution.predict_AQI
                                 ).outerjoin(City, City.id == Pollution.city_id).outerjoin(Time,
                                                                                           Time.id == Pollution.time_id).filter(
                City.name == city,
                extract('year', Time.Dates) == year).all()
            session.commit()
            return aqis

    def get_aqi_by_month_city(self, month, city):
        with self.get_db() as session:
            aqis = session.query(Pollution.AQI
                                 ).outerjoin(City, City.id == Pollution.city_id).outerjoin(Time,
                                                                                           Time.id == Pollution.time_id).filter(
                City.name == city,
                extract('month', Time.Dates) == month).all()
            session.commit()
            return aqis

    def get_all_aqi_by_city(self, city):
        with self.get_db() as session:
            aqis = session.query(Pollution.AQI).outerjoin(City, City.id == Pollution.city_id).outerjoin(Time,
                                                                                                        Time.id == Pollution.time_id).filter(
                City.name == city, Time.Datetimes.is_(None)).all()
            session.commit()
            return aqis

    def get_all_dates(self):
        with self.get_db() as session:
            aqis = session.query(Time.Dates).filter(Time.Datetimes.is_(None)).all()
            session.commit()
            return aqis


class InformationModel(dbSession):
    def add_data(self, obj: information_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Information(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_information_by_date(self, dates):
        with self.get_db() as session:
            informations = session.query(Information.U, Information.V, Information.TEMP, Information.RH,
                                         Information.PSFC, City.lon, City.lat
                                         ).outerjoin(Pollution, Pollution.id == Information.pollution_id).outerjoin(
                Time,
                Time.id == Pollution.time_id).outerjoin(
                City, City.id == Pollution.city_id).filter(
                Time.Dates == dates).all()
            session.commit()
            return informations


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

    def get_all_city(self):
        with self.get_db() as session:
            names = session.query(City.name).order_by(City.id).filter().all()
            session.commit()
            return names


class TimeModel(dbSession):
    def add_time(self, obj: time_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Time(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def judge_time_exist(self, type: int, times):
        with self.get_db() as session:
            if type == 0:
                id = session.query(Time.id).filter(Time.Dates == times).first()
            else:
                id = session.query(Time.id).filter(Time.Datetimes == times).first()
            session.commit()
            return id

    def get_time_id_by_time(self, type, TIME):
        with self.get_db() as session:
            if type == 0:
                id = session.query(Time.id).filter(Time.Dates == TIME).first()
            else:
                id = session.query(Time.id).filter(Time.Datetimes == TIME).first()
            session.commit()
            return id


class FileModel(dbSession):
    def add_file(self, obj: file_interface):  # 用户上传文件(在file表中添加一个记录)
        obj_dict = jsonable_encoder(obj)
        obj_add = File(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_file_by_hash(self, obj: hash_interface):  # 根据size与两个hash查询file的id
        with self.get_db() as session:
            id = session.query(File.id).filter(
                File.size == obj.size,
                File.hash_md5 == obj.hash_md5,
                File.hash_sha256 == obj.hash_sha256).first()
            session.commit()
            return id

    def get_file_info_by_id(self, id: int):
        with self.get_db() as session:
            id = session.query(File.hash_md5, File.hash_sha256, File.name, File.type).filter(
                File.id == id).first()
            session.commit()
            return id


class EventModel(dbSession):
    def add_event(self, obj: event_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Event(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_event_by_city_time(self, city: str, times):
        with self.get_db() as session:
            time_alias1 = aliased(Time, name="time_alias1")
            time_alias2 = aliased(Time, name="time_alias2")
            events = session.query(Event.events).join(City, City.id == Event.city_id).join(time_alias1,
                                                                                           time_alias1.id == Event.begin_time_id).join(
                time_alias2, time_alias2.id == Event.end_time_id).filter(
                City.name == city,
                between(times, time_alias1.Dates, time_alias2.Dates)
            ).all()

            session.commit()
            return events


class GptModel(dbSession):
    def add_content(self, obj: gpt_interface):  # 用户添加gpt回答
        obj_dict = jsonable_encoder(obj)
        obj_add = Gpt(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_content(self):
        with self.get_db() as session:
            id = session.query(Gpt.ask_content, Gpt.reply_content, Gpt.file_id, Gpt.create_dt).filter().all()
            session.commit()
            return id
