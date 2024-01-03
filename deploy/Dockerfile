FROM ubuntu:latest

# 安装环境
RUN apt-get update && \
    apt-get install -y sudo vim redis-server mysql-server npm nodejs dnf uvicorn nginx wget pkg-config python3-pip libmysqlclient-dev locales && locale-gen en_US.UTF-8 zh_CN.UTF-8 && \
    apt-get -y autoclean && \
    sudo chmod 777 /etc/redis
    
# 配置redis
COPY redis.conf /etc/redis/redis.conf

# 配置mysql
COPY mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
RUN  chmod 777 /var/log/mysql && touch /var/log/mysql/mysql-bin.log

# 配置minio
WORKDIR /home/ubuntu/
COPY minio.rpm ./minio.rpm
RUN dnf install -y ./minio.rpm && \
    rm ./minio.rpm && \
    mkdir -p ./minio/data && \
    chmod 777 ./minio ./minio/data && \
    touch ./minio/data/minio.log
ENV MINIO_ROOT_USER=VAOAP-admin \
    MINIO_ROOT_PASSWORD=VAOAPminio123! \
    PATH=${PATH}:./Visual_analysis_of_air_pollution-frontend \
    PYTHONPATH=${PYTHONPATH}:./Visual_analysis_of_air_pollution-backend/ \
    LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:en \
    LC_ALL=zh_CN.UTF-8 \
    ID=""

# 配置项目
COPY Visual_analysis_of_air_pollution-frontend ./Visual_analysis_of_air_pollution-frontend
COPY Visual_analysis_of_air_pollution-backend ./Visual_analysis_of_air_pollution-backend

# 配置前端
RUN npm install -g n && \
    n 18.16.1 && \
    ln -s /usr/local/bin/node /usr/local/bin/nodejs && \
    hash -r && \
    npm install -g yarn && yarn global add serve
COPY default /etc/nginx/sites-available/default
COPY nginx.conf /etc/nginx/nginx.conf

# 配置后端
WORKDIR /home/ubuntu/Visual_analysis_of_air_pollution-backend/
RUN python3 -m venv venv && \
/bin/bash -c "source venv/bin/activate  && \
pip install --upgrade pip && \
pip install -r ./requirements.txt"

# 启动服务
COPY init.sql start.sh data_init.sql  ./../
CMD ["/home/ubuntu/start.sh","--param", "$ID"]

EXPOSE 80