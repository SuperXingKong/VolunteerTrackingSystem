import imp
from flask import Flask, jsonify, render_template, request
# from urllib import parse
# parse.quote(str)
import database
import function

app = Flask(__name__)

# 创造数据库类，之后获取数据等操作直接调用db.function()即可
db=database.Database()
# 创建网络类，仅处理前端传来的数据，network类里面就是纯粹的python解题方法，更加清楚
# 这样，index.py里的部分仅负责将前端传来的数据解包为需要用到的变量，传入function.network进行后续处理
network=function.Network(db)

# 网站主页
@app.route('/')
def sheet():
    return render_template('volunteer.html')

# 传数据模块，把表格数据发给客户端
@app.route('/jsondata', methods=['POST', 'GET'])
def infos():
    # 解包获取数据limit,offset和search
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        search = info.get('search','')
    # 传入network进行处理
    return network.jsondataPacket(limit,offset,search)

# 管理员操作模块,后期功能,现在暂时不考虑,只写了一个删除的功能
@app.route('/admin')
def admin():
    # 解包获取数据action
    if request.method=='GET':
        info = request.values
        action = info.get('action', '')  # 操作名称
        if action == 'del':
            id=info.get('id',0)  # 要删除的学号
            # 传入network进行处理
            network.delData(id)
        elif action == 'login':
            username=info.get('username','')
            password=info.get('password','')
            # TODO: 登录系统，只有管理员有权限做编辑
            network.doLogin(username,password)
    return render_template('volunteer.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
