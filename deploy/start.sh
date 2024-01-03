#!/bin/bash
ID=$ID
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="Visual_analysis_of_air_pollution"
DB_USER="root"
DB_PASSWORD="VAOAPmysql123!"
service mysql start
sleep 5
result=$(mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password="$DB_PASSWORD" -e "SHOW DATABASES LIKE '${DB_NAME}'")
if [  -z "${result}"  ]; then
    if [ "$ID" = "6" ]; then
        sed -i "s/41011/41016/g" /etc/nginx/sites-available/default
        sed -i "s/41011/41016/g" ./const.py
    else
        sed -i "s/41011/4101${ID}/g" /etc/nginx/sites-available/default
        sed -i "s/41011/4101${ID}/g" ./const.py
        sed -i "20i\read-only=1" /etc/mysql/mysql.conf.d/mysqld.cnf
    fi
    sed -i "s/server-id=1/server-id=${ID}/g" /etc/mysql/mysql.conf.d/mysqld.cnf
    sed -i "s|//172.16.2.1|//172.16.2.${ID}|g" ./const.py
    yarn --cwd /home/ubuntu/Visual_analysis_of_air_pollution-frontend/ build
    yarn global add serve
    redis-server /etc/redis/redis.conf --requirepass VAOAPredis123! &
    rm -rf /var/lib/mysql/auto.cnf
    service mysql restart
    sleep 5
    mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password="$DB_PASSWORD" < ../init.sql
    if [ "$ID" = "6" ]; then
        mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password="$DB_PASSWORD" < ../master.sql
    else
        mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password="$DB_PASSWORD" < ../slave.sql
    fi
    service nginx start
    nohup minio server --address 127.0.0.1:9000  ../minio/data > ../minio/data/minio.log 2>&1 &
    source venv/bin/activate
    source ~/.bashrc
    nohup celery -A Celery.upload_file worker --loglevel=INFO -P eventlet > /home/ubuntu/Visual_analysis_of_air_pollution-backend/Celery/upload_file_celery.log 2>&1 &
    nohup celery -A Celery.spider_data worker --loglevel=INFO -P eventlet > /home/ubuntu/Visual_analysis_of_air_pollution-backend/Celery/spider_data_celery.log 2>&1 &
    if [ "$ID" = "6" ]; then
        python3 ./model/db_init.py
        mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password="$DB_PASSWORD" < ../data_init.sql
    fi
    python3 main.py 
else
    if [ "$ID" != "6" ]; then
        mysql -h $DB_HOST -P $DB_PORT -u $DB_USER --password="$DB_PASSWORD" -e "START SLAVE;"
    fi
    yarn --cwd /home/ubuntu/Visual_analysis_of_air_pollution-frontend/ build
    yarn global add serve
    redis-server /etc/redis/redis.conf --requirepass VAOAPredis123! &
    service nginx start
    nohup minio server --address 127.0.0.1:9000  ../minio/data > ../minio/data/minio.log 2>&1 &
    source venv/bin/activate
    nohup celery -A Celery.upload_file worker --loglevel=INFO -P eventlet > /home/ubuntu/Visual_analysis_of_air_pollution-backend/Celery/upload_file_celery.log 2>&1 &
    nohup celery -A Celery.spider_data worker --loglevel=INFO -P eventlet > /home/ubuntu/Visual_analysis_of_air_pollution-backend/Celery/spider_data_celery.log 2>&1 &
    python3 main.py 
fi

