FROM python

COPY requirements.txt .
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple mysqlclient cryptography 
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . ./YiCloud

EXPOSE 6666

RUN chmod +x /YiCloud/main.sh
#CMD ["python3", "/YiCloud/main.py"]
CMD ["sh","/YiCloud/main.sh"]
