CREATE USER 'replication_root'@'%' IDENTIFIED WITH mysql_native_password BY 'VAOAPmysql123!';
GRANT REPLICATION SLAVE ON *.* TO 'replication_root'@'%';
FLUSH PRIVILEGES;

