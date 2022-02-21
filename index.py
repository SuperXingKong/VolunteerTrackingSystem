import imp
from flask import Flask, jsonify, render_template, request
import sqlite3
# from urllib import parse
# parse.quote(str)

app = Flask(__name__)

# 数据库查询到的数据默认是元组形式，如果想json输出需要转字典
# 相当于写了一个方法来替换connect中的row_factory方法
def dict_factory(cursor, row):
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

table_name="volunteerTime"
con = sqlite3.connect(table_name,check_same_thread=False)
con.row_factory=dict_factory
cur = con.cursor()
tmp = cur.execute("select max(rowid) from {}".format(table_name)).fetchone()
totalid = tmp['max(rowid)']

@app.route('/jsondata', methods=['POST', 'GET'])
def infos():
    lastsearch = ''
    lasttotal = 0
    # if request.method == 'POST':
    #     print('post')
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        search = info.get('search','')
    A=int(offset)+2127407001
    B=(int(offset) +2127407000+ int(limit))
    #没有数据库筛选时，用 selector = con.select(select="*", table_name=table_name, where="id BETWEEN "+str(A)+" AND "+str(B))
    if search=='':
        # 分页代码
        selector = "SELECT * FROM {} WHERE (学号 BETWEEN {} AND {})".format(table_name,A,B)
        total = totalid
    else:
        pass
        # TODO: 搜索代码
    # 防止恶意用户一次访问超过100条数据，对服务器造成过大压力
    result = cur.execute(selector).fetchmany(100)
    return jsonify({'total': total, 'rows': result})
    # return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
    # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了

# 管理员操作模块,后期功能,现在暂时不考虑,只写了一个删除的功能
@app.route('/admin')
def admin():
    if request.method=='GET':
        info = request.values
        action = info.get('action', '')  # 操作名称
        if action == 'del':
            id=info.get('id',0)  # 要删除的元素id
            selector="DELETE FROM {} WHERE ID = {}".format(table_name,id)
            cur.execute(selector)
            con.commit()
            print('已删除')
    return render_template('volunteer.html')

# 网站主页
@app.route('/')
def sheet():
    return render_template('volunteer.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
