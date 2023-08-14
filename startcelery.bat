@echo off
if "%1"=="h" goto begin
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin

start celery -A d2Form.celery worker -l info -P eventlet >>work.out
start celery -A d2Form.celery beat -l info >>beat.out

::celery -A d2Form.celery worker -l info -Q d2Form,default -n work1 -P eventlet
::celery -A d2Form.celery worker -l info -Q beat_tasks -n work2 -P eventlet
::celery -A d2Form.celery flower --basic_auth=admin:admin123