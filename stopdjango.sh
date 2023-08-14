#kill -9 $(ps -ef|grep manage.py|grep v|awk '{print $2}')
kill -9 $(ps -ef|grep 'bin/gunicorn'|grep v|awk '{print $2}')
