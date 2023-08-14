CREATE USER 'root'@'%' IDENTIFIED BY 'admin';
GRANT All privileges ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;