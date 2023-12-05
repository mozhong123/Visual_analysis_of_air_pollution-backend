import os
import re
from datetime import datetime, date
from type.functions import evaluate_air_quality
from fastapi import APIRouter
from utils.response import data_standard_response
from type.data import pollution_interface, information_interface, city_interface, time_interface
from service.data import PollutionModel, InformationModel, CityModel, TimeModel
import json

datas_router = APIRouter()

city_model = CityModel()
time_model = TimeModel()
pollution_model = PollutionModel()
information_model = InformationModel()


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
    else:
        time = datetime(2013, 1, day, hour, 0, 0)
        type = 1
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
    pollutions = pollution_model.get_predict_aqi_by_month_city(month, city)
    res = []
    for pollution in pollutions:
        res.append(pollution._asdict())
    return {'data': res, 'message': '结果如下', 'code': 0}


@datas_router.get("/weather_map")
@data_standard_response
async def get_weather_map(dates: date):
    weathers = information_model.get_information_by_date(dates)
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
    for i in range(2013,2019):
        right = 366
        if i == 2016:
            right = 367
        temp = []
        for j in range(1,right):
            temp.append(pollutions[sum][0])
            sum += 1
        res[i] = temp
    return {'data': res, 'message': '结果如下', 'code': 0}