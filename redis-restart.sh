kill -9 $(ps -ef|grep redis|grep v|awk '{print $2}')
cd /etc/redis/
redis-server redis.conf &
