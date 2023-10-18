import hashlib
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    VARCHAR,
    ForeignKey, Date, Index, Float, event, func,
)

from model.db import Base


def encrypted_password(password, salt):  # 对密码进行加密
    res = hashlib.sha256()
    password += salt
    res.update(password.encode())
    return res.hexdigest()


class User(Base):  # 用户表
    __tablename__ = 'user'
    __table_args__ = (
        Index('ix_user_has_delete_username', "has_delete", "username"),  # 非唯一的联合索引
        Index('ix_user_has_delete_email', "has_delete", "email")
    )
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    username = Column(VARCHAR(32), nullable=False, unique=True, comment='用户名')  # 用户名，非空，唯一
    password = Column(VARCHAR(128), nullable=False, comment='密码')  # 密码，非空
    email = Column(VARCHAR(64), nullable=False, unique=True, comment='邮箱地址')  # 邮箱，非空，唯一
    registration_dt = Column(DateTime, nullable=False, comment='注册时间，新建时自动填写', default=func.now())  # 注册时间，非空
    status = Column(Integer, nullable=False, index=True,
                    comment='是否已经禁用:0 正常使用,1 账号未激活,2 账号已注销,3 账号被封禁,', default=1)  # 账号状态，非空
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否被删除，非空


@event.listens_for(User, 'before_insert')  # 再插入前自动加密
def auto_encrypted_password(mapper, connection, target):
    target.password = encrypted_password(target.password, target.username)




class Operation(Base):  # 操作表
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    service_type = Column(Integer, nullable=False, index=True, comment='业务类型')  # 业务类型，非空，索引
    service_id = Column(Integer, nullable=True, comment='业务id')  # 业务id，可空
    operation_type = Column(VARCHAR(64), comment='操作类型', nullable=False)  # 操作类型
    func = Column(VARCHAR(128), comment='操作', nullable=False)  # 操作
    parameters = Column(VARCHAR(4 * 1024), comment='操作参数', nullable=False)  # 操作参数
    oper_user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True,
                          comment='操作人 id，外键')  # 操作人 id，外键，非空，索引
    oper_dt = Column(DateTime, nullable=False, comment='操作时间')
    oper_hash = Column(VARCHAR(128), index=True, comment='操作哈希值' ,nullable=False)  # 操作哈希值，索引


class Session(Base):  # session表
    __tablename__ = 'session'
    __table_args__ = (
        Index('ix_session_has_delete_token_s6', "has_delete", "token_s6"),  # 非唯一的联合索引
        Index('ix_session_has_delete_token', "has_delete", "token"),  # 非唯一的联合索引
        Index('ix_session_func_type_has_delete', "func_type", "has_delete"),  # 非唯一的联合索引
    )
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, comment='外键，用户id')  # 外键，用户id，非空，索引
    file_id = Column(Integer, ForeignKey('user_file.id'), nullable=True, index=True,
                     comment='外键，文件id')  # 外键，文件id，可空，索引
    token = Column(VARCHAR(32), unique=True, nullable=False, comment='session唯一识别串')  # token，非空，唯一
    token_s6 = Column(VARCHAR(16), nullable=True, comment='8位短token')  # 邮箱验证码，非空
    use = Column(Integer, nullable=False, comment='使用次数')  # 使用次数，非空
    use_limit = Column(Integer, nullable=True, comment='限制次数，没有限制即为NULL')  # 限制次数，可空
    exp_dt = Column(DateTime, comment='过期时间', nullable=False)  # 过期时间，非空
    ip = Column(VARCHAR(32), comment='客户端ip')  # ip
    user_agent = Column(VARCHAR(256), comment='客户端信息')  # 客户端信息
    create_dt = Column(DateTime, comment='创建时间', default=func.now())  # 创建时间
    func_type = Column(Integer,
                       comment='0 用户登录 session:1 用户邮箱验证 session,2 文件下载 session,3 文件上传 session')  # 操作类型
    has_delete = Column(Integer, nullable=False, comment='是否已经删除', default=0)  # 是否已经删除