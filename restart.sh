cd /home/d2Form
echo "redis restart"
sh redis-restart.sh
sleep 1
echo "celery restart"
sh restartcelery.sh
sleep 1
echo "django restart"
python38 manage.py migrate
python38 manage.py init
sh stopdjango.sh
sh startdjango.sh
sleep 1
echo "nginx restart"
sh nginx-restart.sh
