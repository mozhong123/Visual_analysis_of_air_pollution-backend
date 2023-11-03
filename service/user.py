from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from model.user import User
from model.db import dbSession



class UserModel(dbSession):

    def add_user(self, obj: user_add_interface):  # 管理员添加一个用户(在user表中添加一个用户)
        obj_dict = jsonable_encoder(obj)
        obj_add = User(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def add_all_user(self, user_list):  # 管理员批量添加用户
        objects = [User(**jsonable_encoder(user_list[i])) for i in range(len(user_list))]
        with self.get_db() as session:
            session.add_all(objects)
            session.flush()
            session.commit()
            return objects

    def delete_user(self, id: int):  # 删除一个用户
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"has_delete": 1})
            session.commit()
            return id

    def update_user_status(self, id: int, status: int):  # 更改用户账号状态
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"status": status})
            session.commit()
            return id

    def update_user_storage_quota(self, id: int, storage_quota: int):  # 更改用户存储空间限制
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"storage_quota": storage_quota})
            session.commit()
            return id

    def update_user_password(self, id: int, password: str):  # 更改用户密码
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"password": password})
            session.commit()
            return id

    def update_user_username(self, id: int, username: str):  # 更改用户名
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"username": username})
            session.commit()
            return id

    def update_user_email(self, id: int, email: str):  # 更改绑定邮箱
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"email": email})
            session.commit()
            return id

    def update_user_card_id(self, id: int, card_id: str):  # 更改学号
        with self.get_db() as session:
            session.query(User).filter(User.id == id).update({"card_id": card_id})
            session.commit()
            return id

    def get_user_by_username(self, username):  # 根据username查询user的基本信息
        with self.get_db() as session:
            user = session.query(User).filter(User.has_delete == 0, User.username == username).first()
            session.commit()
            return user

    def get_user_some_by_username(self, username):  # 根据username查询user的部分信息
        with self.get_db() as session:
            user = session.query(User.email, User.password, User.username, User.id).filter(User.has_delete == 0,
                                                                                                 User.username == username).first()
            session.commit()
            return user

    def get_user_email_by_username(self, username):  # 根据username查询id,email
        with self.get_db() as session:
            email = session.query(User.id, User.email).filter(User.username == username).first()
            session.commit()
            return email

    def get_user_status_by_username(self, username):  # 根据username查询user的帐号状态
        with self.get_db() as session:
            user = session.query(User.status).filter(User.has_delete == 0, User.username == username).first()
            session.commit()
            return user

    def get_user_by_email(self, email):  # 根据email查询user的基本信息
        with self.get_db() as session:
            user = session.query(User).filter(User.has_delete == 0, User.email == email).first()
            session.commit()
            return user

    def get_user_status_by_email(self, email):  # 根据email查询user的帐号状态
        with self.get_db() as session:
            user = session.query(User.status).filter(User.has_delete == 0, User.email == email).first()
            session.commit()
            return user

    def get_user_status_by_card_id(self, card_id):  # 根据card_id查询user的帐号状态
        with self.get_db() as session:
            user = session.query(User.status).filter(User.has_delete == 0, User.card_id == card_id).first()
            session.commit()
            return user

    def get_user_id_by_email(self, email):  # 根据email查询user_id
        with self.get_db() as session:
            user = session.query(User.id).filter(User.has_delete == 0, User.email == email).first()
            session.commit()
            return user

    def get_user_by_user_id(self, user_id):  # 根据user_id查询user的基本信息
        with self.get_db() as session:
            user = session.query(User).filter(User.id == user_id, User.has_delete == 0).first()
            session.commit()
            return user

    def get_user_all_information_by_user_id(self, user_id):  # 根据user_id查询user的所有信息
        with self.get_db() as session:
            informations = session.query(User.username, User.email, User.card_id, User.registration_dt,
                                         User_info.realname, User_info.gender, School.name, College.name, Major.name,
                                         Class.name, User_info.enrollment_dt, User_info.graduation_dt). \
                outerjoin(User_info, User_info.user_id == User.id). \
                outerjoin(Major, Major.id == User_info.major_id). \
                outerjoin(Class, Class.id == User_info.class_id). \
                outerjoin(College, College.id == Major.college_id). \
                outerjoin(School, School.id == College.school_id). \
                filter(User.id == user_id, User.has_delete == 0). \
                first()
            session.commit()
            return informations

    def get_user_information_by_id(self, user_id):  # 根据user_id查询user的所有信息
        with self.get_db() as session:
            user = session.query(User, User_info).outerjoin(User_info, User_info.user_id == User.id).filter(
                User.id == user_id,
                User.has_delete == 0
            ).first()
            session.commit()
            return user

    def get_user_status_by_user_id(self, user_id):  # 根据user_id查询user的帐号状态
        with self.get_db() as session:
            status = session.query(User.status).filter(User.id == user_id, User.has_delete == 0).first()
            session.commit()
            return status

    def get_name_by_user_id(self, user_id):  # 根据user_id查询username,realname
        with self.get_db() as session:
            names = session.query(User.username, User_info.realname).outerjoin(User_info,
                                                                               User_info.user_id == user_id).filter(
                User.id == user_id, User.has_delete == 0).first()
            session.commit()
            return names

    def get_user_name_by_user_id(self, user_id):  # 根据user_id查询username
        with self.get_db() as session:
            name = session.query(User.username).filter(
                User.id == user_id, User.has_delete == 0).first()
            session.commit()
            return name


class SessionModel(dbSession):
    def add_session(self, obj: session_interface):  # 添加一个session
        obj_dict = jsonable_encoder(obj)
        obj_dict['exp_dt'] = func.from_unixtime(obj_dict['exp_dt'])
        obj_add = Session(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def add_all_session(self, sessions):  # 批量添加session
        objects = [Session(**jsonable_encoder(sessions[i])) for i in range(len(sessions))]
        with self.get_db() as session:
            session.add_all(objects)
            session.flush()
            session.commit()
            return 'ok'

    def delete_session(self, id: int):  # 根据id删除一个session
        with self.get_db() as session:
            session.query(Session).filter(Session.id == id).update({"has_delete": 1})
            session.commit()
            return id

    def delete_session_by_token(self, token: str):  # 根据token删除一个session
        with self.get_db() as session:
            session.query(Session).filter(Session.token == token).update({"has_delete": 1})
            session.commit()
            return 'ok'

    def get_session_by_token(self, token):  # 根据token查询session的基本信息
        with self.get_db() as session:
            ses = session.query(Session).filter(Session.has_delete == 0, Session.token == token).first()
            session.commit()
            return ses

    def get_user_id_by_token(self, token):  # 根据token查询user_id
        with self.get_db() as session:
            user_id = session.query(Session.user_id).filter(Session.has_delete == 0, Session.token == token).first()
            session.commit()
            return user_id

    def get_session_by_id(self, id):  # 根据id查询session的基本信息
        with self.get_db() as session:
            ses = session.query(Session).filter(Session.id == id, Session.has_delete == 0).first()
            session.commit()
            return ses

    def update_session_use(self, id: int, use_add: int):  # 根据id更改session中的use
        with self.get_db() as session:
            session.query(Session).filter(Session.id == id).update({"use": Session.use + use_add})
            session.commit()
            return id

    def update_session_use_by_token(self, token: str, use_add: int):  # 根据token更改session中的use by token
        with self.get_db() as session:
            session.query(Session).filter(Session.token == token).update({"use": Session.use + use_add})
            session.commit()
            return "ok"

    def update_session_use_limit(self, id: int, use_limit: int):  # 更改session中的use_limit
        with self.get_db() as session:
            session.query(Session).filter(Session.id == id).update({"use_limit": use_limit})
            session.commit()
            return id

    def add_new_something(self, new):
        with self.get_db() as session:
            session.add(new)
            session.flush()
            session.commit()
            return new.id


class UserinfoModel(dbSession):
    def add_userinfo(self, obj: user_info_interface):  # 在user_info表中添加一条信息
        obj_dict = jsonable_encoder(obj)
        obj_dict.pop('card_id')
        new_user_info = model.user.User_info(**obj_dict)
        # 在user_info表中新建一个
        return self.add_new_something(new_user_info)

    def add_all_user_info(self, user_info_list, user_id_list):  # 管理员批量添加user_info
        objects = []
        for i in range(len(user_info_list)):
            obj_dict = jsonable_encoder(user_info_list[i])
            obj_dict.pop('card_id')
            obj_dict['user_id'] = user_id_list[i].id
            objects.append(User_info(**obj_dict))
        with self.get_db() as session:
            session.add_all(objects)
            session.flush()
            session.commit()
            return 'ok'

    def delete_userinfo(self, id: int):  # 删除一条信息
        with self.get_db() as session:
            session.query(User_info).filter(User_info.id == id).update({"has_delete": 1})
            session.commit()
            return id

    def delete_userinfo_by_user_id(self, user_id: int):  # 删除一条信息
        with self.get_db() as session:
            session.query(User_info).filter(User_info.user_id == user_id).update({"has_delete": 1})
            session.commit()
            return 'ok'

    def update_userinfo_realname(self, id: int, realname: str):  # 更改用户真实名字
        with self.get_db() as session:
            session.query(User_info).filter(User_info.id == id).update({"realname": realname})
            session.commit()
            return id

    def update_userinfo_gender(self, id: int, gender: int):  # 更改用户性别
        with self.get_db() as session:
            session.query(User_info).filter(User_info.id == id).update({"gender": gender})
            session.commit()
            return id

    def update_userinfo_major(self, id: int, major_id: int):  # 更改用户专业
        with self.get_db() as session:
            session.query(User_info).filter(User_info.id == id).update({"major_id": major_id})
            session.commit()
            return id

    def update_userinfo_class(self, id: int, class_id: int):  # 更改用户班级
        with self.get_db() as session:
            session.query(User_info).filter(User_info.id == id).update({"class_id": class_id})
            session.commit()
            return id

    def get_userinfo_by_user_id(self, user_id):  # 根据user_id查询user的基本信息
        with self.get_db() as session:
            userinfo = session.query(User_info).filter(User_info.user_id == user_id, User_info.has_delete == 0).first()
            session.commit()
            return userinfo

    def get_major_id_by_user_id(self, user_id):  # 根据user_id查询user的major_id
        with self.get_db() as session:
            userinfo = session.query(User_info.major_id).filter(User_info.user_id == user_id,
                                                                User_info.has_delete == 0).first()
            session.commit()
            return userinfo

    def get_userinfo_by_id(self, id):  # 根据id查询userinfo的基本信息
        with self.get_db() as session:
            userinfo = session.query(User).filter(User_info.id == id, User_info.has_delete == 0).first()
            session.commit()
            return userinfo

    def add_new_something(self, new):
        with self.get_db() as session:
            session.add(new)
            session.flush()
            session.commit()
            return new.id


class OperationModel(dbSession):
    def add_operation(self, obj: operation_interface):  # 添加一个操作(在operation表中添加一个操作)
        obj.oper_hash = obj.get_oper_hash()
        obj_dict = jsonable_encoder(obj)
        obj_add = Operation(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def get_operation_hash_by_id(self, id):  # 根据id查询operation的hash
        with self.get_db() as session:
            hash = session.query(Operation.oper_hash).filter(Operation.id == id).first()
            session.commit()
            return hash

    def get_func_and_time_by_admin(self, page, user_id):  # 查找某操作人的所有操作和时间
        with self.get_db() as session:
            operations = session.query(Operation.func,Operation.oper_dt).filter(
                Operation.oper_user_id == user_id).order_by(
                Operation.id).offset(
                page.offset()).limit(page.limit()).all()
            session.commit()
            return operations

    def get_operation_by_service(self, service_type, service_id):  # 根据service查询operation的基本信息
        with self.get_db() as session:
            operation = session.query(Operation).filter(Operation.service_type == service_type,
                                                        Operation.service_id == service_id).first()
            session.commit()
            return operation

    def get_operation_by_service_type(self, service_type, service_id, type):  # 根据service与type查询operation的基本信息
        with self.get_db() as session:
            reason = session.query(Operation.func, Operation.oper_user_id).filter(
                Operation.service_type == service_type,
                Operation.service_id == service_id, Operation.operation_type == type).first()
            session.commit()
            return reason

    def get_operation_by_oper_user_id(self, oper_user_id):  # 根据user_id查询operation的基本信息
        with self.get_db() as session:
            operation = session.query(Operation).filter(Operation.oper_user_id == oper_user_id).first()
            session.commit()
            return operation

    def get_operation_by_hash(self, oper_hash):  # 根据hash查询operation的parameters
        with self.get_db() as session:
            operation = session.query(Operation.parameters).filter(Operation.oper_hash == oper_hash).first()
            session.commit()
            return operation

    def get_operation_by_id(self, id):  # 根据id查询operation的基本信息
        with self.get_db() as session:
            operation = session.query(Operation).filter(Operation.id == id).first()
            session.commit()
            return operation


class CaptchaModel(dbSession):
    def add_captcha(self, value):  # 添加一个验证码
        obj_add = Captcha(value=value, has_delete=0)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def delete_captcha(self, id: int):  # 删除一个captcha
        with self.get_db() as session:
            session.query(Captcha).filter(Captcha.id == id).update({"has_delete": 1})
            session.commit()
            return id

    def get_captcha_by_id(self, id):  # 根据id查询captcha的值
        with self.get_db() as session:
            value = session.query(Captcha.value).filter(Captcha.id == id, Captcha.has_delete == 0).first()
            session.commit()
            return value


class EducationProgramModel(dbSession):
    def add_education_program(self, obj: education_program_interface):  # 添加一个培养方案
        obj_dict = jsonable_encoder(obj)
        obj_add = Education_Program(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.flush()
            session.commit()
            return obj_add.id

    def delete_education_program(self, id: int):  # 删除一个education_program
        with self.get_db() as session:
            session.query(Education_Program).filter(Education_Program.id == id).update({"has_delete": 1})
            session.commit()
            return id

    def get_education_program_by_user_id(self, user_id):  # 根据user_id查询education_program
        with self.get_db() as session:
            user_info = UserinfoModel()
            major_id = user_info.get_major_id_by_user_id(user_id)
            if major_id is None:
                return 0
            value = session.query(Education_Program).filter(
                Education_Program.has_delete == 0,
                Education_Program.major_id == major_id[0]).first()
            session.commit()
            if value:
                # 使用字典推导式创建带有属性名的字典
                result_dict = {key: getattr(value, key) for key in value.__dict__ if
                               not key.startswith('_') and getattr(value, key) is not None}
                translated_result = {programs_translation1.get(key, key): value for key, value in result_dict.items()}
                session.commit()
                return translated_result
            else:
                return None

    def get_exist_education_program_by_major_id(self, major_id):  # 根据major_id查询education_program是否存在
        with self.get_db() as session:
            value = session.query(Education_Program.has_delete).filter(Education_Program.major_id == major_id).first()
            session.commit()
            return value

    def update_education_program_exist(self, major_id: int):  # 更改education_program存在状态
        with self.get_db() as session:
            session.query(Education_Program).filter(Education_Program.major_id == major_id).update({"has_delete": 0})
            session.commit()
            return 'ok'
