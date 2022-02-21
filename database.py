import sqlite3

# 这个对象整合了需要进行的所有数据库操作，在index.py里只负责实现功能而不需要考虑如何使用数据库语言
class Database:
    #数据库文件名称
    file_name=""
    #表的名称
    table_name=""
    #临时数据
    tmp = []
    #整个表的数据条数
    totalid = 0
    #self.con是数据库连接
    #self.cur是连接的游标

    # 建立数据库连接和初始化
    def __init__(self,file_name="volunteerTime",table_name="volunteerTime"):
        self.file_name=file_name
        self.table_name=table_name
        self.con = sqlite3.connect(self.file_name,check_same_thread=False)

        # 数据库查询到的数据默认是元组形式，如果想json输出需要转字典
        def dict_factory(cursor, row):
            data = {}
            for idx, col in enumerate(cursor.description):
                data[col[0]] = row[idx]
            return data
        # 这一句，相当于写了一个方法来替换connect对象中的row_factory方法，让下面的getPlayer()返回值为字典
        self.con.row_factory=dict_factory

        self.cur = self.con.cursor()
        self.tmp = self.cur.execute("select max(rowid) from {}".format(self.table_name)).fetchone()
        self.totalid = self.tmp['max(rowid)']

    def getUser(self,id):
        selector = "SELECT * FROM {} WHERE 学号 = {}".format(self.table_name,id)
        return self.cur.execute(selector).fetchone()
    # 例如，调用函数getPlayer(2127407017)，返回的结果为一个字典：
    # {'学号': '2127407017', '姓名': '卞佳骏', '班级': '21AI1班', '心理讲座（活动）': '', 
    # '冬至活动（活动）': '3', '羽毛球（活动）': '', '排球（活动）': '', '足球（活动）': '26', 
    # '乒乓球（活动）': '', '篮球（活动）': '', '新舞（活动）': '', '团日活动（活动）': '3', 
    # '新生英语短剧（活动）': '', '班团干部（活动）': '7', '逐光摄影（活动）': '4', '唐仲英（活动）': '', 
    # '新媒体（活动）': '2', '团支部（公益）': '', '新媒体（公益）': '4', '青委志愿时长认定会议（公益）': '6', 
    # '开学新生引导（公益）': '', '唐仲英（公益）': '', '学生工作处（公益）': '', '写未来学院建设提议书（公益）': '', 
    # '未来校区志愿服务（公益）': '', '人大选举（公益）': '4', '智工舍值班（公益）': '', '冬至活动（公益）': '', 
    # '献血（公益）': '', '未来学院院旗的制作（公益）': '', '班团干部（公益）': '7', '活动时长': '45', 
    # '公益时长': '21', '总时长': '66'}
    
    # 从表中顺序获取从第begin条到第end条数据并返回（这里的begin和end是以学号为关键字）
    # 返回的值是一个列表，里面套着每个学生的数据字典
    def getUserList(self,begin,end):
        selector = "SELECT * FROM {} WHERE (学号 BETWEEN {} AND {})".format(self.table_name,begin,end)
        # 最多获取100条数据
        return self.cur.execute(selector).fetchmany(100)

    # 从表中搜索姓名中含search的条目，返回条目数量
    def searchUserNumber(self,search):
        selector = "SELECT COUNT(姓名) AS TOTAL FROM {} WHERE (姓名 LIKE '%{}%')".format(self.table_name,search)
        self.tmp=self.cur.execute(selector).fetchone()
        total = self.tmp['TOTAL']
        # 返回条目数量
        return total

    # 从表中搜索姓名中含search的条目，从搜索到的结果中第offset条开始，顺序获取limit条数据并返回（这里的offset和limit仅代表数量而不是学号）
    # 返回的值是一个字典
    def searchUserList(self,search,offset,limit):
        selector= "SELECT * FROM {} WHERE (姓名 LIKE '%{}%') LIMIT {} OFFSET {}".format(self.table_name,search,limit,offset)
        return self.cur.execute(selector).fetchmany(100)

    def addUser(self,id,dic):
        pass

    # 删除学号为id的那条数据
    def delUser(self,id):
        selector="DELETE FROM {} WHERE 学号 = {}".format(self.table_name,id)
        self.cur.execute(selector)
        return self.con.commit()
