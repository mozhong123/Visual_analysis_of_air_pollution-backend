import base64
import copy
import io
from datetime import date
import speech_recognition as sr
import requests
import pandas as pd
from minio import S3Error
from starlette.responses import JSONResponse

from model.db import minio_client

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
import numpy as np
import time
import random
import re
import os
import json
from const import api_key
from bs4 import BeautifulSoup


# 通过经纬度获得城市名和城市地址（省市区）
def get_address(lat, lng, ak):
    url = f"https://api.map.baidu.com/reverse_geocoding/v3/?ak={ak}&output=json&coordtype=wgs84ll&location={lat},{lng}"
    response = requests.get(url)
    data = response.json()
    city = data['result']['addressComponent']['city']  # 解析城市名
    address = data['result']['formatted_address']  # 解析地址
    return city, address


def process_csv_ult(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines.pop(0)
        for line in lines:
            # 去除行尾换行符
            line = line.rstrip('\n')
            # 分割行数据
            row = line.split(',')
            # 去除空数据和首尾空白字符
            cleaned_row = [value.strip() for value in row if value.strip()]
            # 添加非空数据行到结果列表
            if cleaned_row:
                data.append(cleaned_row)
    return {'data': data}


def write_to_json(data, file_path):
    # 经纬度提到前面
    processed_data = {key: [values[12:17] + values[1:12] for values in rows] for key, rows in data.items()}
    # 字符串转float，去掉了数据上的双引号
    json_str = json.dumps(processed_data, ensure_ascii=False)
    # 使用正则表达式去除数字的双引号
    # 将字符串类型的数字转换为浮点数类型
    data_obj = json.loads(json_str)
    # 将字符串类型的数字转换为浮点数类型
    data_obj["data"] = [[float(num) if isinstance(num, str) and (num.replace('.', '', 1).isdigit() or (
            num.startswith('-') and num[1:].replace('.', '', 1).isdigit())) else num for num in sublist] for sublist
                        in data_obj["data"]]
    json_data = json.dumps(data_obj, ensure_ascii=False)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_data)


def make_json():
    # 替换成自己的ak
    ak = ['1',
          '2',
          '3',
          '4',
          '5',
          '6',
          '7',
          '8',
          '9']
    # 读取文档
    df = pd.read_csv("D:/A学习资料A/大三上/大数据分析实践/2014/CN-Reanalysis2013010100.csv", encoding="utf-8")
    # 将文档中每一行经纬度，请求接口，返回并打印数据
    city_list = []
    address_list = []
    i = 0
    for index, row in df.iterrows():
        if index == 0:
            ak1 = ak[0]
            print("0")
        elif index % 5000 == 0:
            i = i + 1
            ak1 = ak[i]
            print(i)
        lat = row[11]
        lng = row[12]
        city1, address1 = get_address(lat, lng, ak1)
        # 将数据加入列表中
        city_list.append(city1)
        address_list.append(address1)
        sleep_time = random.uniform(0.04, 0.2)
        time.sleep(sleep_time)  # 个人开发者API请求每秒最多30次，休息一下
    print("end")
    # 将城市地址添加到 DataFrame 中
    df['city'] = city_list
    df['address'] = address_list
    # 将两列写入文档中
    df.to_csv("D:/A学习资料A/大三上/大数据分析实践/2014_json/cc_2013010100.csv", index=False)
    city_list = [' '] * 42249
    address_list = [' '] * 42249
    for i in range(0, 42249):
        city_list[i] = str(df['city'][i])
        address_list[i] = str(df['address'][i])
        if city_list[i] == 'nan':
            city_list[i] = address_list[i]

    # 待处理的CSV文件夹路径
    csv_folder = "D:/A学习资料A/大三上/大数据分析实践/2013_temp"
    # 待输出的JSON文件夹路径
    output_folder = "D:/A学习资料A/大三上/大数据分析实践/2013_t1/"
    # 获取CSV文件夹中的所有CSV文件
    csv_files = [file for file in os.listdir(csv_folder) if file.endswith('.csv')]
    # 处理每个CSV文件
    for csv_file in csv_files:
        file_path_input = os.path.join(csv_folder, csv_file)
        file_path_output = os.path.join(output_folder, csv_file)
        file = pd.read_csv(file_path_input)
        file['city'] = city_list
        file['address'] = address_list
        file.to_csv(file_path_output)
    # 待处理的CSV文件夹路径
    csv_folder = "D:/A学习资料A/大三上/大数据分析实践/2013_t1/"
    # 待输出的JSON文件夹路径
    output_folder = "D:/A学习资料A/大三上/大数据分析实践/2013_ultra/"
    # 获取CSV文件夹中的所有CSV文件
    csv_files = [file for file in os.listdir(csv_folder) if file.endswith('.csv')]
    # 处理每个CSV文件
    for csv_file in csv_files:
        file_path = os.path.join(csv_folder, csv_file)
        output_file_path = os.path.join(output_folder, csv_file.replace('.csv', '.json'))
        result = process_csv_ult(file_path)
        write_to_json(result, output_file_path)


def evaluate_air_quality(aqi):
    if 0 <= aqi <= 50:
        return "优秀"
    elif 51 <= aqi <= 100:
        return "良好"
    elif 101 <= aqi <= 150:
        return "轻度污染"
    elif 151 <= aqi <= 200:
        return "中度污染"
    elif 201 <= aqi <= 300:
        return "重度污染"
    else:
        return "严重污染"


def get_date(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'aqi_query_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTZiZjQ1MWI5NjUzZWNiZDA0MzIzMzllMWUxMWRjYmZiBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUxuYkg4V0tMV2xMeXFBb2NFNDViMHRWTklPRE5lMUxEQ01OQmd2VXFELzg9BjsARg%3D%3D--a08f667c6f9b040442ae1daab0fc5c45641db6bf; __utma=162682429.909376057.1565782011.1565782011.1565782011.1; __utmc=162682429; __utmz=162682429.1565782011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=162682429.1.10.1565782011',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    dates = []
    try:
        if response.status_code == 200:
            response = response.text
            soup = BeautifulSoup(response, 'lxml')
            dates_ = soup.find_all('li')
            for i in dates_:
                if i.a:  # 去除空值
                    li = i.a.text  # 提取li标签下的a标签
                    date = re.findall('[0-9]*', li)  # ['2019', '', '12', '', '']
                    year = date[0]
                    month = date[2]
                    if month and year:  # 去除不符合要求的内容
                        date_new = '-'.join([year, month])
                        dates.append(date_new)
            return dates
    except:
        print('数据获取失败！')


def spider(url, Date, browser, times):
    year = Date.year
    month = Date.month
    tempDate = date(year, month, 1)
    browser.get(url)
    df = pd.read_html(browser.page_source, header=0)[0]  # 返回第一个Dataframe
    time.sleep(1.5)
    if not df.empty:
        columnindex = 0
        for index, row in df.head(1).iterrows():
            for column, value in row.items():
                if value == tempDate.strftime(
                        "%Y-%m-%d"):
                    columnindex = df.columns.get_loc(column)
                    break
        num_columns = len(df.columns)
        # 循环移位操作
        for i in range(columnindex):
            temp = copy.deepcopy(df.iloc[:, 0])
            df.iloc[:, 0:num_columns - 1] = df.iloc[:, 1:num_columns].values
            # 将最左边的列移动到最右边
            df.iloc[:, -1] = temp
        df = df[df['日期'] == Date.strftime("%Y-%m-%d")]
        return df[['日期', 'AQI', 'NO2', 'PM10', 'PM2.5', 'SO2', 'CO', 'O3_8h', '质量等级']]
    else:
        end_time = time.time()
        execution_time = end_time - times
        if execution_time >= 5:
            return None
        else:
            return spider(url, Date, browser, times)  # 防止网络还没加载出来就爬取下一个url


def voice2text(file_bytes):
    r = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(file_bytes)) as source:
        audio = r.record(source)
    query = '请帮我具体分析一下这张图'
    try:
        query = r.recognize_google(audio, language='zh-CN')
    except Exception as e:
        return query
    return query


def send2gpt(text, image_file_content):
    base64_image = base64.b64encode(image_file_content).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }
    response = requests.post("https://oneapi.xty.app/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']


def get_files(object_key,type):  # 根据桶名称与文件名从Minio上下载文件
    try:
        object_data = minio_client.get_object('main', object_key)
        content = object_data.read()
        if type == 0:
            return content
        else:
            return io.BytesIO(content)
    except S3Error as e:
        return JSONResponse(content={'message': e, 'code': 3, 'data': False})