CREATE DATABASE visual_analysis_of_air_pollution;
CREATE USER 'admin'@'%' IDENTIFIED BY 'VAOAPmysql123!';
GRANT ALL PRIVILEGES ON visual_analysis_of_air_pollution.* TO 'admin'@'%';
FLUSH PRIVILEGES;