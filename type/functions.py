import requests
import pandas as pd
import numpy as np
import time
import random
import re
import os
import json


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
