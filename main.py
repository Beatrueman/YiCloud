# -*- coding: utf-8 -*-
from routes.index import index, app
from routes.dashboard import db

# 登录与注册
app.register_blueprint(index)

# 用户界面及功能
app.register_blueprint(db)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 6666)
