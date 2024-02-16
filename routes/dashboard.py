from flask import Blueprint, send_file, url_for
from flask import render_template, request, session, jsonify
from flask_login import current_user, login_required
import os

db = Blueprint('dashboard', __name__)


@login_required
@db.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = current_user.username
    session['current_user'] = username
    return render_template('dashboard.html', username=username)

# 上传文件
@db.route('/dashboard/upload', methods=['GET','POST'])
def upload():
    file = request.files['file']

    if current_user.is_authenticated:
        username = current_user.username
        user_folder = os.path.abspath("data/{}".format(username))

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        file.save(os.path.join(user_folder, file.filename))
        
        print("上传成功！")
        return jsonify(success=True)
    else:
        return jsonify(success=False)

# 文件列表
@db.route('/dashboard/files',methods=['GET','POST'])
def get_filesList():
    if current_user.is_authenticated:
        username = current_user.username
        user_folder = os.path.join("data/{}".format(username))

        files_list = os.listdir(user_folder)
        files_dict = {'files': files_list}

        return jsonify(files_dict)
    else:
        return "Login required"

# 下载文件
@db.route('/dashboard/download/<filename>', methods=['GET'])
def download(filename):
    username = current_user.username
    user_folder = os.path.abspath('data/{}'.format(username))
    file_path = os.path.join(user_folder, filename)
    print(file_path,user_folder)

    # 检查文件是否存在
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True) # as_attachment=True提示用户下载文件
    else:
        return "未找到文件！"
    
@db.route('/dashboard/getfiles', methods=['GET'])
def get_files():
    if current_user.is_authenticated:
        username = current_user.username
        user_folder = os.path.join('data', username)
        file_list = os.listdir(user_folder)

        per_page = 7  # 每页显示7个数据
        page = request.args.get('page', 1, type=int)

        start_index = (page - 1) * per_page # 每页的起始文件数据索引
        end_index = start_index + per_page

        paginated_files = file_list[start_index:end_index]

        total_pages = (len(file_list) + per_page - 1) // per_page  # 计算总页数

        files_with_links = []
        for filename in paginated_files:
            download_link = url_for('dashboard.download', filename=filename)
            files_with_links.append({'filename': filename, 'download_link': download_link})
            print(jsonify({'files': files_with_links, 'total_pages': total_pages}))
            
        return jsonify({'files': files_with_links, 'total_pages': total_pages})
    else:
        return "Login required"

# 删除文件
@db.route('/dashboard/delete/<filename>', methods=['DELETE'])
def delete(filename):
    if current_user.is_authenticated:
        username = current_user.username
        user_folder = os.path.join('data',username)
        file_path = os.path.join(user_folder, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify(success=True)
        else:
            return jsonify(success=False)
        

