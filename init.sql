ALTER USER 'root'@'%' IDENTIFIED BY 'YiCloud*123456';
-- 这一条命令一定要有：
flush privileges;

CREATE USER 'cloud'@'%' IDENTIFIED BY 'YiCloud*123456';

CREATE DATABASE cloud;

USE cloud;

GRANT ALL PRIVILEGES ON cloud.* TO 'cloud'@'%';

flush privileges;

