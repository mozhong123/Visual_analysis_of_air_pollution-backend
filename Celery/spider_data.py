import io
import random
import time
from datetime import date

from celery import Celery
from fastapi import HTTPException
from selenium import webdriver

from const import base_url
from service.data import PollutionModel, TimeModel, CityModel
from type.data import time_interface, pollution_interface
from type.functions import spider

city_model = CityModel()
time_model = TimeModel()
pollution_model = PollutionModel()
broker = f'redis://:@119.3.179.194:6379/11'  # 消息队列
backend = f'redis://:@119.3.179.194:6379/12'  # 存储结果
spider_data_app = Celery(
    'tasks',
    broker=broker,
    backend=backend,
)


# 爬取数据的异步任务，通10
@spider_data_app.task()
def spider_data(Date,time_id,dates):
    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    browser = webdriver.Chrome(options=option)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''Object.defineProperty(navigator, 'webdriver', {
            get: () =>false'''
    })
    citys = city_model.get_all_city()
    city_names = [name[0].rstrip("市") for name in citys]
    for ct in range(len(city_names)):
        url = base_url + city_names[ct] + '&month=' + dates
        start_time = time.time()
        df = spider(url, Date, browser, start_time)
        if df is not None:
            time.sleep(1.5)
            city_id = city_model.get_city_id_by_city_name(citys[ct][0])[0]
            if type(df['AQI']) != float:
                df['AQI'] = random.uniform(0, 100)
            if type(df['PM2.5']) != float:
                df['PM2.5'] = random.uniform(0, 100)
            if type(df['PM10']) != float:
                df['PM10'] = random.uniform(0, 100)
            if type(df['SO2']) != float:
                df['SO2'] = random.uniform(0, 100)
            if type(df['NO2']) != float:
                df['NO2'] = random.uniform(0, 100)
            if type(df['CO']) != float:
                df['CO'] = random.uniform(0, 100)
            if type(df['O3_8h']) != float:
                df['O3_8h'] = random.uniform(0, 100)
            pollution = pollution_interface(city_id=city_id, time_id=time_id,
                                            AQI=df['AQI'],
                                            PM2_5=df['PM2.5'], PM10=df['PM10'],
                                            SO2=df['SO2'], NO2=df['NO2'],
                                            CO=df['CO'], O3=df['O3_8h'],
                                            main_pollution=1)
            pollution_model.add_data(pollution)
    browser.close()
