CHANGE MASTER TO 
MASTER_HOST='119.3.179.194',
MASTER_PORT = 3306,
MASTER_USER='replication_root', 
MASTER_PASSWORD='VAOAPmysql123!',
MASTER_LOG_FILE='mysql-bin.000002', 
MASTER_LOG_POS=1060521; 
START SLAVE;