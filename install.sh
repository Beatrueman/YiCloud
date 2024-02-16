#!/bin/bash

echo "======欢迎安装YiCloud======"

echo "======进行数据库初始化======"

echo "请输入数据库主机host："
read host

echo "请输入数据库用户名："
read user

echo "请输入数据库密码："
read password

echo "请输入数据库数据库名："
read database

echo "数据库默认端口为3306"

echo "host = '$host'" > config.py
echo "user = '$user'" >> config.py
echo "password = '$password'" >> config.py
echo "database = '$database'" >> config.py

if [ -f config.py ]; then
    echo "数据库配置信息已保存到config.py文件中"
else
    echo "保存数据库配置信息到config.py文件失败"
    exit 1
fi

python3 database_init.py

echo "======安装Python依赖库======"
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo "======启动YiCloud======"
python3 main.py
