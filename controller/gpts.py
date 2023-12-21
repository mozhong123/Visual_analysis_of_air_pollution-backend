import json
from hashlib import md5, sha256
from fastapi import APIRouter
from fastapi import UploadFile, File, Form
from Celery.upload_file import upload_file
from model.db import gpt_db
from service.data import PollutionModel, InformationModel, CityModel, TimeModel, FileModel, EventModel, GptModel
from type.data import file_interface, hash_interface, gpt_interface
from type.functions import send2gpt, voice2text, get_files
from utils.response import data_standard_response

gpts_router = APIRouter()

city_model = CityModel()
time_model = TimeModel()
pollution_model = PollutionModel()
information_model = InformationModel()
file_model = FileModel()
event_model = EventModel()
gpt_model = GptModel()


@gpts_router.post("/ask_gpt_by_content")
@data_standard_response
async def ask_gpt_by_content(gpt_ask: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    md5_hash = md5()
    md5_hash.update(contents)
    md5_hexdigest = md5_hash.hexdigest()
    sha256_hash = sha256()
    sha256_hash.update(contents)
    sha256_hexdigest = sha256_hash.hexdigest()
    exist_file = file_model.get_file_by_hash(
        hash_interface(size=file.size, hash_md5=md5_hexdigest, hash_sha256=sha256_hexdigest))
    # if exist_file is not None:
    #     return {'message': '文件已存在', 'data': False, 'code': 1}
    folder = md5_hexdigest[:8] + '/' + sha256_hexdigest[-8:] + '/'  # 先创建路由
    upload_file.delay(folder, file.filename, contents)
    add_file = file_interface(size=file.size,
                              hash_md5=md5_hexdigest,
                              hash_sha256=sha256_hexdigest,
                              name=file.filename,
                              type=file.content_type)
    id = file_model.add_file(add_file)
    reply_content = send2gpt(gpt_ask, contents)
    gpt_end = gpt_interface(ask_content=gpt_ask, reply_content=reply_content, file_id=id)
    gpt_model.add_content(gpt_end)
    return {'message': '结果如下', 'data': {'reply_content':reply_content}, 'code': 0}


@gpts_router.post("/ask_gpt_by_voice")
@data_standard_response
async def ask_gpt_by_voice(voice: UploadFile = File(...), file: UploadFile = File(...)):
    contents = await file.read()
    voice_contents = await voice.read()
    md5_hash = md5()
    md5_hash.update(contents)
    md5_hexdigest = md5_hash.hexdigest()
    sha256_hash = sha256()
    sha256_hash.update(contents)
    sha256_hexdigest = sha256_hash.hexdigest()
    exist_file = file_model.get_file_by_hash(
        hash_interface(size=file.size, hash_md5=md5_hexdigest, hash_sha256=sha256_hexdigest))
    # if exist_file is not None:
    #     return {'message': '文件已存在', 'data': False, 'code': 1}
    folder = md5_hexdigest[:8] + '/' + sha256_hexdigest[-8:] + '/'  # 先创建路由
    upload_file.delay(folder, file.filename, contents)
    add_file = file_interface(size=file.size,
                              hash_md5=md5_hexdigest,
                              hash_sha256=sha256_hexdigest,
                              name=file.filename,
                              type=file.content_type)
    id = file_model.add_file(add_file)
    ask_content = voice2text(voice_contents)
    reply_content = send2gpt(ask_content,contents)
    gpt_end = gpt_interface(ask_content=ask_content, reply_content=reply_content, file_id=id)
    gpt_model.add_content(gpt_end)
    return {'message': '结果如下', 'data': {'reply_content':reply_content}, 'code': 0}



@gpts_router.get("/gpt_content")
@data_standard_response
async def get_gpt_content():
    all_gpts = gpt_model.get_content()
    res = []
    for gpt_information in all_gpts:
        res.append({'ask_content':gpt_information.ask_content,'reply_content':gpt_information.reply_content,'url':'http://127.0.0.1:8000/files/download/'+str(gpt_information.file_id),'create_dt':gpt_information.create_dt.strftime(
                "%Y-%m-%d %H:%M:%S")})
    return {'data': res, 'message': '结果如下', 'code': 0}