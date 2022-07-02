from openpyxl import Workbook,load_workbook
from itertools import islice
import CONST

class DatabaseExcel:
    def __init__(self,file_name="2022-6.xlsx"):
        self.wb = load_workbook(file_name, data_only=True)  # 该方法主要用于导入一个已经存在的工作薄
        self.nametoid = {}
        self.updateNameToId()
    
    def updateNameToId(self):
        
        for sheet in self.wb:
            for row in islice(sheet.rows, 1, None):
                if self.nametoid.get(row[1].value):
                    self.nametoid[row[1].value] = self.nametoid[row[1].value] + (int(row[0].value),)
                else:
                    self.nametoid[row[1].value] = (int(row[0].value),)
    def getLastEditedSheet(self):
        return self.wb.active
    
    def getClassById(self, id):
        prefix = id // 100
        postfix = id % 100
        if prefix in CONST.IDTOCLASS.keys():
            d = CONST.IDTOCLASS[prefix]
            for values in d:
                if postfix <= values[0]:
                    return values[1]
        else:
            return False

    def getLineById(self, id):
        sheet = self.wb[self.getClassById(id)]
        #TODO: 改为二分搜索
        for row in islice(sheet.rows, 1, None):
            if int(row[0].value)==id:
                n=row
                break
            
        data = []  # 存放读取的行数据
        for i in row:  # 'Sheet'为表单名称, 1 为第一行
            data.append(i.value)
        return data

    def getLineByName(self, name):
        ids = self.nametoid[name]
        result = []
        for id in ids:
            result.append(self.getLineById(id))
        return result
        


db  =  DatabaseExcel()
print(db.getLineByName('孙宇栋'))