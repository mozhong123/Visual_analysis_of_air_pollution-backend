import io
import os
import random
import re
import time
from datetime import datetime, date
from hashlib import md5, sha256

import pandas as pd
from fastapi import Request, UploadFile, File, Form
from selenium import webdriver
from Celery.spider_data import spider_data
from Celery.upload_file import upload_file
from model.db import event_db, rank_db
from type.functions import evaluate_air_quality, spider, send2gpt, voice2text, get_files
from fastapi import APIRouter
from utils.response import data_standard_response
from type.data import pollution_interface, information_interface, city_interface, time_interface, date_interface, \
    file_interface, event_interface, hash_interface, events_interface, gpt_interface, gpt
from service.data import PollutionModel, InformationModel, CityModel, TimeModel, FileModel, EventModel, GptModel
import json

datas_router = APIRouter()

city_model = CityModel()
time_model = TimeModel()
pollution_model = PollutionModel()
information_model = InformationModel()
file_model = FileModel()
event_model = EventModel()
gpt_model = GptModel()


@datas_router.post("/add_datas")
@data_standard_response
async def add_datas():
    # 指定文件夹路径
    folder_path1 = __file__ + '\\..\\..\\data\\2013'
    folder_path2 = __file__ + '\\..\\..\\data\\2013-2018'
    # 使用 os.listdir() 列出文件夹中的文件
    files1 = os.listdir(folder_path1)
    for file in files1:
        file_path = os.path.join(folder_path1, file)
        pattern = r'(\d{2})(\d{2})\.json'  # 匹配两个数字，然后再匹配两个数字后面的 ".json"
        match = re.search(pattern, file)
        day = int(match.group(1))
        hour = int(match.group(2))
        time = time_interface(Datetimes=datetime(2013, 1, day, hour, 0, 0))
        time_id = time_model.add_time(time)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        for i in range(len(data['data'])):
            city_id = city_model.get_city_id_by_city_name(data['data'][i][4])
            if city_id is None:
                city = city_interface(name=data['data'][i][4], lon=data['data'][i][1], lat=data['data'][i][0])
                city_id = city_model.add_city(city)
            else:
                city_id = city_id[0]
            pollution = pollution_interface(city_id=city_id, time_id=time_id,
                                            AQI=data['data'][i][2],
                                            PM2_5=data['data'][i][5], PM10=data['data'][i][6],
                                            SO2=data['data'][i][7], NO2=data['data'][i][8],
                                            CO=data['data'][i][9], O3=data['data'][i][10],
                                            main_pollution=data['data'][i][3])
            pollution_id = pollution_model.add_data(pollution)
            information = information_interface(U=data['data'][i][11], V=data['data'][i][12], TEMP=data['data'][i][13],
                                                RH=data['data'][i][14], PSFC=data['data'][i][15],
                                                pollution_id=pollution_id)
            information_model.add_data(information)
    years = os.listdir(folder_path2)
    # 遍历文件列表
    for year in years:
        folder_path3 = folder_path2 + '\\' + year
        months = os.listdir(folder_path3)
        for month in months:
            file_path = os.path.join(folder_path3, month)
            pattern = r'(\d{2})(\d{2})00.json'  # 匹配两个数字，然后再匹配两个数字后面的 ".json"
            match = re.search(pattern, month)
            Day = int(match.group(2))
            Month = int(match.group(1))
            time = time_interface(Dates=date(int(year), Month, Day))
            time_id = time_model.add_time(time)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            for i in range(len(data['data'])):
                city_id = city_model.get_city_id_by_city_name(data['data'][i][4])
                if city_id is None:
                    city = city_interface(name=data['data'][i][4], lon=data['data'][i][1], lat=data['data'][i][0])
                    city_id = city_model.add_city(city)
                else:
                    city_id = city_id[0]
                pollution = pollution_interface(city_id=city_id, time_id=time_id,
                                                AQI=data['data'][i][2],
                                                PM2_5=data['data'][i][5], PM10=data['data'][i][6],
                                                SO2=data['data'][i][7], NO2=data['data'][i][8],
                                                CO=data['data'][i][9], O3=data['data'][i][10],
                                                main_pollution=data['data'][i][3])
                pollution_id = pollution_model.add_data(pollution)
                information = information_interface(U=data['data'][i][11], V=data['data'][i][12],
                                                    TEMP=data['data'][i][13],
                                                    RH=data['data'][i][14], PSFC=data['data'][i][15],
                                                    pollution_id=pollution_id)
                information_model.add_data(information)
    return {'data': True, 'message': '数据添加成功', 'code': 0}


@datas_router.get("/pollution")
@data_standard_response
async def get_pollution(city: str, year: int = None, month: int = None, day: int = None, hour: int = None):
    if hour is None:
        time = date(year, month, day)
        type = 0
    else:
        time = datetime(2013, 1, day, hour, 0, 0)
        type = 1
    pollutions = pollution_model.get_pollution_by_city_date(city, time, type)._asdict()
    pollutions['AQIState'] = evaluate_air_quality(pollutions['AQI'])
    return {'data': pollutions, 'message': '结果如下', 'code': 0}


@datas_router.get("/pollution_map")
@data_standard_response
async def get_pollution(year: int = None, month: int = None, day: int = None, hour: int = None):
    if hour is None:
        time = date(year, month, day)
        type = 0
        id = time_model.judge_time_exist(0, time)
        if id is None:
            return {'data': None, 'message': '暂无该天数据，您可尝试获取', 'code': 1}
    else:
        time = datetime(2013, 1, day, hour, 0, 0)
        type = 1
        id = time_model.judge_time_exist(0, time)
        if id is None:
            return {'data': None, 'message': '暂无该天数据，您可尝试获取', 'code': 1}
    pollutions = pollution_model.get_pollution_by_date(time, type)
    res = []
    for pollution in pollutions:
        pollution = pollution._asdict()
        pollution['AQIState'] = evaluate_air_quality(pollution['AQI'])
        res.append(pollution)
    return {'data': res, 'message': '结果如下', 'code': 0}


@datas_router.get("/reality_predict_AQI")
@data_standard_response
async def get_reality_predict(year: int, city: str):
    pollutions = pollution_model.get_two_aqi_by_year_city(year, city)
    res = []
    for pollution in pollutions:
        res.append(pollution._asdict())
    return {'data': res, 'message': '结果如下', 'code': 0}


@datas_router.get("/predict_AQI")
@data_standard_response
async def get_reality_predict(month: int, city: str):
    pollutions = pollution_model.get_aqi_by_month_city(month, city)
    res = []
    for pollution in pollutions:
        res.append(pollution._asdict())
    return {'data': res, 'message': '结果如下', 'code': 0}


@datas_router.get("/weather_map")
@data_standard_response
async def get_weather_map(year: int, month: int, day: int):
    time = date(year, month, day)
    weathers = information_model.get_information_by_date(time)
    res = []
    for pollution in weathers:
        res.append(pollution._asdict())
    return {'data': res, 'message': '结果如下', 'code': 0}


@datas_router.get("/all_AQI")
@data_standard_response
async def get_all_AQI(city: str):
    pollutions = pollution_model.get_all_aqi_by_city(city)
    res = {}
    sum = 0
    for i in range(2013, 2019):
        right = 366
        if i == 2016:
            right = 367
        temp = []
        for j in range(1, right):
            temp.append(pollutions[sum][0])
            sum += 1
        res[i] = temp
    return {'data': res, 'message': '结果如下', 'code': 0}


@datas_router.post("/spider_day_data")
@data_standard_response
async def spider_datas(date_data: date_interface):
    dates = "{:04d}{:02d}".format(date_data.year, date_data.month)
    Date = date(date_data.year, date_data.month, date_data.day)
    id = time_model.judge_time_exist(0, Date)
    if id is not None:
        return {'data': None, 'message': '已有该天数据，您无需爬取', 'code': 1}
    time_id = time_model.add_time(time_interface(Dates=Date))
    spider_data.delay(Date, time_id, dates)
    return {'message': '爬取成功，请稍后查看', 'data': True, 'code': 0}


@datas_router.post("/add_events_file")
@data_standard_response
async def add_events(file: UploadFile = File(...)):
    contents = await file.read()
    md5_hash = md5()
    md5_hash.update(contents)
    md5_hexdigest = md5_hash.hexdigest()
    sha256_hash = sha256()
    sha256_hash.update(contents)
    sha256_hexdigest = sha256_hash.hexdigest()
    exist_file = file_model.get_file_by_hash(
        hash_interface(size=file.size, hash_md5=md5_hexdigest, hash_sha256=sha256_hexdigest))
    if exist_file is not None:
        return {'message': '文件已存在', 'data': False, 'code': 1}
    folder = md5_hexdigest[:8] + '/' + sha256_hexdigest[-8:] + '/'  # 先创建路由
    upload_file.delay(folder, file.filename, contents)
    add_file = file_interface(size=file.size,
                              hash_md5=md5_hexdigest,
                              hash_sha256=sha256_hexdigest,
                              name=file.filename,
                              type=file.content_type)
    id = file_model.add_file(add_file)
    contents = contents.decode("utf-8")
    df = pd.read_csv(io.StringIO(contents))
    for index, row in df.iterrows():
        # 在这里可以访问每一行的数据
        # 可以使用row['列名']来获取每一列的值
        city = row['城市']
        start_date = datetime.strptime(row['起始时间'], "%Y/%m/%d").date()
        end_date = datetime.strptime(row['终止时间'], "%Y/%m/%d").date()
        event_description = row['事件描述']
        city_id = city_model.get_city_id_by_city_name(city)
        if city_id is not None:
            begin_time_id = time_model.get_time_id_by_time(0, start_date)[0]
            end_time_id = time_model.get_time_id_by_time(0, end_date)[0]
            event = event_interface(city_id=city_id[0], begin_time_id=begin_time_id, end_time_id=end_time_id,
                                    events=event_description)
            event_model.add_event(event)
    return {'message': '添加成功', 'data': True, 'code': 0}


@datas_router.post("/add_events")
@data_standard_response
async def add_events(events: events_interface):
    city_id = city_model.get_city_id_by_city_name(events.city)
    if city_id is not None:
        begin_time_id = time_model.get_time_id_by_time(0, events.begin_time)[0]
        end_time_id = time_model.get_time_id_by_time(0, events.end_time)[0]
        event = event_interface(city_id=city_id[0], begin_time_id=begin_time_id, end_time_id=end_time_id,
                                events=events.events)
        event_model.add_event(event)
    return {'message': '添加成功', 'data': True, 'code': 0}


@datas_router.get("/events")
@data_standard_response
async def get_events(city: str, year: int = None, month: int = None, day: int = None):
    time = date(year, month, day)
    func = city + time.strftime("%Y-%m-%d")
    redis_event = event_db.get(func)  # 有效session中没有
    if redis_event is not None:
        events = json.loads(redis_event.decode("utf-8").replace("'", "\""))  # 登陆了就返回用户登录的session
    else:
        temp_events = event_model.get_event_by_city_time(city, time)
        events = None
        if temp_events:
            events = []
            for event in temp_events:
                events.append(event[0])
            event_db.set(func, str(events), ex=1270000)
    return {'message': '结果如下', 'data': events, 'code': 0}


@datas_router.get("/province_rank")
@data_standard_response
async def get_province_rank(year: int = None, month: int = None, day: int = None):
    time = date(year, month, day)
    type = 0
    id = time_model.judge_time_exist(0, time)
    if id is None:
        return {'data': None, 'message': '暂无该天数据，您可尝试获取', 'code': 1}
    redis_rank = rank_db.get(time.strftime("%Y-%m-%d"))  # 有效session中没有
    if redis_rank is not None:
        res = json.loads(redis_rank.decode("utf-8").replace("'", "\""))
    else:
        pollutions = pollution_model.get_rank_by_date(time, type)
        res = []
        for pollution in pollutions:
            pollution = pollution._asdict()
            res.append(pollution)
        rank_db.set(time.strftime("%Y-%m-%d"), str(res), ex=1270000)
    return {'data': res, 'message': '结果如下', 'code': 0}
