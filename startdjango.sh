cd /home/d2Form
rm -rf djo.out
#nohup python manage.py runserver 0.0.0.0:8000 >djo.out 2>&1 &
nohup gunicorn d2Form.asgi:application -w 2 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 >djo.out 2>&1 &
