import base64
import json
import random
import string
import uuid
from io import BytesIO
from captcha.image import ImageCaptcha
from fastapi import APIRouter
from fastapi import Request, Header, Depends
from model.user import encrypted_password
from type.page import page
from utils.response import user_standard_response, page_response, makePageResult

users_router = APIRouter()


'''
# 验证用户用户名，邮箱，学号的唯一性
@users_router.post("/unique_verify")
@user_standard_response
async def user_unique_verify():


# 获得图片验证码
@users_router.get("/get_captcha")
@user_standard_response
async def get_captcha():
    characters = string.digits + string.ascii_uppercase  # characters为验证码上的字符集，10个数字加26个大写英文字母
    width, height, n_len, n_class = 170, 80, 4, len(characters)  # 图片大小
    generator = ImageCaptcha(width=width, height=height)
    random_str = ''.join([random.choice(characters) for j in range(4)])  # 生出四位随机数字与字母的组合
    img = generator.generate_image(random_str)
    img_byte = BytesIO()
    img.save(img_byte, format='JPEG')  # format: PNG or JPEG
    binary_content = img_byte.getvalue()  # im对象转为二进制流
    captcha = random_str
    id = captcha_model.add_captcha(captcha)
    img_base64 = base64.b64encode(binary_content).decode('utf-8')
    src = f"data: image/jpeg;base64,{img_base64}"
    return {'data': {'captcha': src, 'captchaId': str(id)}, 'message': '获取成功', 'code': 0}


# 验证图片验证码是否正确并发送邮箱验证码
@users_router.post("/send_captcha")
@user_standard_response
async def send_captcha(captcha_data: captcha_interface, request: Request, user_agent: str = Header(None)):
    value = captcha_model.get_captcha_by_id(int(captcha_data.captchaId))
    if value[0] != captcha_data.captcha:
        return {'message': '验证码输入错误', 'code': 1, 'data': False}
    id = None
    str1 = ''
    str2 = ''
    token = str(uuid.uuid4().hex)  # 生成token
    email_token = get_email_token()
    if captcha_data.type == 0:  # 用户首次登陆时发邮件
        user_information = user_model.get_user_email_by_username(captcha_data.username)
        if user_information is None:  # 看看有没有这个用户名
            return {'data': False, 'message': '没有该用户', 'code': 1}
        if user_information[1] != captcha_data.email:  # 看看有没有这个邮箱
            return {'data': False, 'message': '邮箱不正确，不是之前绑定的邮箱', 'code': 2}
        id = user_information[0]
        send_email.delay(captcha_data.email, email_token, 0)  # 异步发送邮件
        str1 = f'用户{captcha_data.username}于qpzm7913首次登陆激活账号并向其发送邮件'
        str2 = '激活账号'
    if captcha_data.type == 1:  # 更改邮箱时发邮件
        id = get_user_id(request)
        old_email = user_model.get_user_by_user_id(int(id))  # 新更改邮箱不能与原邮箱相同
        if old_email.email == captcha_data.email:
            return {'message': '不能与原邮箱相同', 'code': 3, 'data': False}
        send_email.delay(captcha_data.email, email_token, 1)  # 异步发送邮件
        str1 = f'用户{captcha_data.username}于qpzm7913修改绑定邮箱{old_email.email}并向新邮箱{captcha_data.email}发送邮件'
        str2 = '修改绑定邮箱'
    elif captcha_data.type == 2:  # 找回密码时发邮件
        id = user_model.get_user_id_by_email(captcha_data.email)[0]
        send_email.delay(captcha_data.email, token, 2)  # 异步发送邮件
        str1 = f'用户{captcha_data.username}于qpzm7913找回密码时向绑定邮箱{captcha_data.email}发送邮件'
        str2 = '找回密码'
    parameters = await make_parameters(request)
    add_operation.delay(0, id, str2,str1, parameters, id)
    session = session_interface(user_id=int(id), ip=request.client.host,
                                func_type=1,
                                token=token, user_agent=user_agent, token_s6=email_token,
                                use_limit=1, exp_dt=get_time_now('minutes',5))  # 新建一个session
    id = session_model.add_session(session)
    session = session.model_dump()
    user_session = json.dumps(session)
    session_db.set(token, user_session, ex=300)  # 缓存有效session(时效5分钟)
    return {'data': True, 'token_header': token, 'message': '验证码已发送，请前往验证！', 'code': 0}


# 用户通过输入邮箱验证码激活
@users_router.put("/activation")
@user_standard_response
async def user_activation(email_data: email_interface, request: Request, type: int = 0):
    token = request.cookies.get("TOKEN")
    session = session_db.get(token)  # 从缓存中得到有效session
    if session is None:
        session_model.delete_session_by_token(token)
        return {'message': '验证码已过期', 'code': 1, 'data': False}
    user_session = session_model.get_session_by_token(token)  # 根据token获取用户的session
    if user_session is None:
        return {'message': '验证码已过期', 'code': 1, 'data': False}
    if session is not None:  # 在缓存中能找到，说明该session有效
        session = json.loads(session)
        if session['token_s6'] == email_data.token_s6:  # 输入的验证码正确
            session_model.update_session_use(user_session.id, 1)  # 把这个session使用次数设为1
            session_model.delete_session(user_session.id)  # 把这个session设为无效
            session_db.delete(token)
            parameters = await make_parameters(request)
            username = get_user_name(user_session.user_id)
            if type == 0:  # 用户激活时进行验证
                user_model.update_user_status(user_session.user_id, 0)
                add_operation.delay(0, user_session.user_id,'通过邮箱验证',f'用户{username}于qpzm7913激活时输入了正确的邮箱验证码{email_data.token_s6}通过验证', parameters,
                                    user_session.user_id)
                return {'message': '验证成功', 'data': True, 'token_header': '-1', 'code': 0}
            if type == 1:  # 修改邮箱时进行验证
                user_model.update_user_email(user_session.user_id, email_data.email)
                add_operation.delay(0, user_session.user_id, '通过邮箱验证',f'用户{username}于qpzm7913修改邮箱时输入了正确的邮箱验证码{email_data.token_s6}通过验证', parameters,
                                    user_session.user_id)
                return {'message': '验证成功', 'data': True, 'token_header': '-1', 'code': 0}
        else:
            return {'message': '验证码输入错误', 'code': 2, 'data': False}
    else:  # 缓存中找不到，说明已无效
        session_model.delete_session(user_session.id)
        return {'message': '验证码已过期', 'code': 1, 'data': False}


# 输入账号密码进行登录
@users_router.post("/login")
@user_standard_response
async def user_login(log_data: login_interface, request: Request, user_agent: str = Header(None),
                     token=Depends(auth_not_login)):
    user_information = user_model.get_user_by_username(log_data.username)  # 先查看要登录的用户名是否存在
    if user_information is None:  # 用户名不存在
        return {'message': '用户名或密码不正确', 'data': False, 'code': 1}
    else:  # 用户名存在
        new_password = encrypted_password(log_data.password, user_information.username)  # 判定输入的密码是否正确
        if new_password == user_information.password:
            status = user_model.get_user_status_by_username(log_data.username)[0]  # 登陆时检查帐号状态
            if status == 1:
                return {'message': '账号未激活', 'data': False, 'code': 2}
            elif status == 2:
                return {'message': '账号已注销', 'data': False, 'code': 3}
            elif status == 3:
                return {'message': '账号被封禁', 'data': False, 'code': 4}
            token = str(uuid.uuid4().hex)
            session = session_interface(user_id=int(user_information.id), ip=request.client.host,
                                        func_type=0,
                                        token=token, user_agent=user_agent, exp_dt=
                        get_time_now('days',14))
            id = session_model.add_session(session)
            session = session.model_dump()
            user_session = json.dumps(session)
            session_db.set(token, user_session, ex=1209600)  # 缓存有效session
            parameters = await make_parameters(request)
            add_operation.delay(0, int(user_information.id), '用户登录',f'用户{log_data.username}于qpzm7913输入了正确的账号和密码进行登录', parameters, int(user_information.id))
            return {'message': '登陆成功', 'token': token, 'data': True, 'code': 0}
        else:
            return {'message': '用户名或密码不正确', 'data': False, 'code': 1}


# 下线
@users_router.put("/logout")
@user_standard_response
async def user_logout(request: Request, session=Depends(auth_login)):
    token = session['token']
    mes = session_model.delete_session_by_token(token)  # 将session标记为已失效
    session_db.delete(token)  # 在缓存中删除
    parameters = await make_parameters(request)
    username = get_user_name(session['user_id'])
    add_operation.delay(0, session['user_id'], '退出登录', f'用户{username}于qpzm7913退出登录',parameters, session['user_id'])
    return {'message': '下线成功', 'data': {'result': mes}, 'token': '-1', 'code': 0}


# 输入原密码与新密码更改密码
@users_router.put("/password_update")
@user_standard_response
async def user_password_update(request: Request, password: password_interface, session=Depends(auth_login)):
    user_id = session['user_id']
    user = user_model.get_user_by_user_id(user_id)
    if user.password != encrypted_password(password.old_password, user.username):  # 原密码输入错误
        return {'message': '密码输入不正确', 'data': False, 'code': 1}
    new_password = encrypted_password(password.new_password, user.username)
    if user.password == new_password:  # 新密码与旧密码相同
        return {'message': '新密码不能与旧密码相同', 'data': False, 'code': 2}
    id = user_model.update_user_password(user_id, new_password)  # 更新新密码
    parameters = await make_parameters(request)
    username = get_user_name(session['user_id'])
    add_operation.delay(0, id,'更改密码', f'用户{username}于qpzm7913通过输入原密码，新密码进行更改密码', parameters, id)
    return {'data': {'user_id': id}, 'message': '修改成功', 'code': 0}


# 输入验证码确认正确后，输入更改邮箱对邮箱进行更改
@users_router.post("/email_update")
@user_standard_response
async def user_email_update(email_data: email_interface, request: Request, session=Depends(auth_login)):
    token = request.cookies.get("TOKEN")
    result = await user_activation(email_data, request, token, 1)  # 验证验证码是否输入正确
    ans = json.loads(result.body)
    user_information = user_information_db.get(session["token"])
    if user_information is not None:
        user_information = json.loads(user_information)
        user_information['email'] = email_data.email
        user_information_db.set(session["token"], json.dumps(user_information), ex=1209600)  # 缓存有效session
    else:
        session_model.delete_session_by_token(session["token"])
    return {'data': True, 'message': ans['message'], 'code': 0}


# 输入用户名，邮箱找回密码
@users_router.post("/get_back_password")
@user_standard_response
async def user_password_get_back(captcha_data: captcha_interface, request: Request, user_agent: str = Header(None)):
    user_information = user_model.get_user_by_username(captcha_data.username)
    if user_information is None:  # 看看有没有这个用户名
        return {'data': False, 'message': '没有该用户', 'code': 1}
    if user_information.email != captcha_data.email:  # 看看有没有这个邮箱
        return {'data': False, 'message': '邮箱不正确，不是之前绑定的邮箱', 'code': 2}
    captcha_data.type = 2
    result = await send_captcha(captcha_data, request, user_agent)
    ans = json.loads(result.body)
    return {'data': True, 'message': ans['message'], 'code': 0}


# 找回密码后用户输入新密码设置密码
@users_router.get("/set_password/{token}")
@user_standard_response
async def user_set_password(request: Request, new_password: str, token: str):
    user_id = session_model.get_user_id_by_token(token)  # 查出user_id
    if user_id is None:
        return {'data': False, 'message': '无法找到该页面', 'code': 1}
    user_id = user_id[0]
    user_information = user_model.get_user_by_user_id(user_id)
    new_password = encrypted_password(new_password, user_information.username)
    if user_information.password == new_password:
        return {'data': False, 'message': '新密码不能与原密码相同', 'code': 2}
    user_model.update_user_password(user_id, new_password)  # 设置密码
    parameters = await make_parameters(request)
    add_operation.delay(0, user_id,'重设密码', f'用户{user_information.username}通过输入新密码进行重设密码', parameters, user_id)
    return {'data': True, 'message': '修改成功', 'code': 0}


# 查看用户信息
@users_router.get("/getProfile")
@user_standard_response
async def user_get_Profile(request:Request,session=Depends(auth_login)):
    data = get_user_information(session['user_id'])
    parameters = await make_parameters(request)
    name = get_user_name(session['user_id'])
    add_operation.delay(0, None, '查看用户信息', f"{name}于qpzm7913查看自己的个人信息", parameters, session['user_id'])
    return {'data': data, 'message': '结果如下', 'code': 0}




@users_router.get("/get_operation/{user_id}")  # 获取用户的所有操作
@page_response
async def user_get_operation(user_id: int, pageNow: int, pageSize: int,request:Request, permission=Depends(auth_login)):
    Page = page(pageSize=pageSize, pageNow=pageNow)
    all_operations = operation_model.get_func_and_time_by_admin(Page, user_id)
    result = {'rows': None}
    if all_operations:
        operation_data = []
        for operation in all_operations:  # 对每个操作的数据进行处理
            dict = {'func': operation[0], 'oper_dt': operation[1].strftime(
                "%Y-%m-%d %H:%M:%S")}
            operation_data.append(dict)
        result = makePageResult(Page, len(all_operations), operation_data)
    parameters = await make_parameters(request)
    name = get_user_name(permission['user_id'])
    name1 = get_user_name(user_id)
    add_operation.delay(1, user_id, '获取用户操作', f"{name}于qpzm7913获取用户{name1}的所有操作", parameters, permission['user_id'])
    return {'message': '操作如下', "data": result, "code": 0}
    
'''
