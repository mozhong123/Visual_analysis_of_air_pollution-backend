from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
from const import SQLALCHEMY_DATABASE_URL
import redis
from minio import Minio, S3Error

minio_client = Minio(
    "119.3.179.194:9000",  # 更新为MinIO服务器的地址和端口
    access_key="minioadmin",  # 你的MinIO访问密钥
    secret_key="minioadmin",  # 你的MinIO秘密密钥
    secure=False  # 是否使用安全连接（根据你的MinIO配置选择）
)
try:
    if not minio_client.bucket_exists('main'):
        minio_client.make_bucket('main')
except S3Error as e:
    print(f'Error: {e}')

pool1 = redis.ConnectionPool(host='119.3.179.194', port=6379, db=1, encoding='UTF-8')
pool2 = redis.ConnectionPool(host='119.3.179.194', port=6379, db=2, encoding='UTF-8')
'''
pool3 = redis.ConnectionPool(host='127.0.0.1', port=6379, db=3, encoding='UTF-8')
user_information_db = redis.Redis(connection_pool=pool2)  # 根据user_id缓存用户基本信息
url_db = redis.Redis(connection_pool=pool3)  # 根据user_file_id缓存下载链接
'''
event_db = redis.Redis(connection_pool=pool1)  # 根据token缓存有效session
rank_db = redis.Redis(connection_pool=pool2)  # 根据token缓存有效session

Base = declarative_base()


class dbSession:
    def __init__(self, db_url=SQLALCHEMY_DATABASE_URL):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        self.SessionThreadLocal = scoped_session(self.SessionLocal)

    @contextmanager
    def get_db(self):
        if self.SessionThreadLocal is None:
            raise Exception("Database not connected")
        session = self.SessionThreadLocal()
        try:
            yield session
        finally:
            session.close()

    def add(self, record):
        with self.get_db() as session:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def delete(self, record):
        record_id = record.id
        with self.get_db() as session:
            session.delete(record)
            session.commit()
            return record_id