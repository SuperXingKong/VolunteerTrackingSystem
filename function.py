
from flask import jsonify


class Network():

    def __init__(self,database):
        self.db=database

    # 给定一个长度limit和开始位置offset，
    # 要求函数返回jsonify({'total': total, 'rows': result})，
    # 其中total为数据的条目数（如果search为空则total为数据库中总条目数，如果search不为空则total为满足搜索条件的总条目数）
    # result是一个列表，格式为[{},{}...{}]，见Database类
    def jsondataPacket(self,limit,offset,search):
        A=int(offset) + 2127407001
        B=(int(offset) + 2127407000 + int(limit))
        if search=='':
            total=self.db.totalid
            result= self.db.getUserList(A,B)
        else:
            total=self.db.searchUserNumber(search)
            result=self.db.searchUserList(search,offset,limit)
        return jsonify({'total': total, 'rows': result})
        # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
        # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了

    def delData(self,id):
        print('已删除学号',id,'的数据')
        return self.db.delUser(id)

    def doLogin(self,username,password):
        pass

class DataTool():
    pass
