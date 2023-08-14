FROM q907305684/d2formvue:1.0
# 运行前需要修改.env.production文件，确定对外服务的IP或者域名，对应端口8082
COPY fronted/.env.production /home/d2Form/fronted
# 校验mysql是否启动的脚本
COPY mysql8/cmd/wait-for-it.sh /wait-for-it.sh
# 构建并初始化程序
RUN /bin/bash /home/d2Form/setup.sh && chmod +x /wait-for-it.sh