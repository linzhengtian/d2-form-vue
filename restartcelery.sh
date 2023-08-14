export C_FORCE_ROOT=true
ps -ef|grep "bin/celery"|grep -v grep|awk '{print $2}'|xargs kill -9 > /dev/null 2>&1
cd /home/d2Form
nohup celery -A d2Form.celery worker -l info > /home/d2Form/logs/worker.log 2>&1 & 
nohup celery -A d2Form.celery beat -l info > /home/d2Form/logs/beat.log 2>&1 & 
