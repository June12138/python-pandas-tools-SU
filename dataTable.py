import pandas as pd

class MyDF(pd.DataFrame):
    idField = 'ID'
    def GetRowByID(self, id):
        return self[self[self.idField] == id]
    def QuickSearch(self, searchField, searchKey, returnKey):
        return self[self[searchField] == searchKey].iloc[0][returnKey]
    def SearchContain(self, searchField, searchKey, returnKey):
        for i in range(0,len(self)):
            currentRow = self.iloc[i]
            if (searchKey in str(currentRow[searchField])):
                return currentRow[returnKey]
    def Compare(self, other):
        output = {}
        # Find common, added, and removed rows
        selfIDList = []
        otherIDList = []
        for i in range(0,len(self)):
            selfIDList.append(self.iloc[i][self.idField].item())
        for i in range(0,len(other)):
            otherIDList.append(other.iloc[i][self.idField].item())
        common_ids = []
        removed_rows = []
        for id in selfIDList:
            if id in otherIDList:
                common_ids.append(id)
            else:
                removed_rows.append(id)
        added_rows = []
        for id in otherIDList:
            if id not in common_ids:
                added_rows.append(id)
        # 不同、添加、和删除的输出变量
        out_difA = MyDF(pd.DataFrame(columns=self.columns))
        out_difB = MyDF(pd.DataFrame(columns=self.columns))
        out_add = MyDF(pd.DataFrame(columns=self.columns))
        out_remove = MyDF(pd.DataFrame(columns=self.columns))
        # 找到有修改的行数
        for i in common_ids:
            selfRow = self[self[self.idField] == i]
            otherRow = other[other[self.idField] == i]
            if not selfRow.equals(otherRow):
                for i in selfRow:
                    if selfRow[i].item() != otherRow[i].item():
                        out_difA = pd.concat([out_difA, selfRow])
                        out_difB = pd.concat([out_difB, otherRow])
                        break
        # 找到B表中增加的行数
        for idx in added_rows:
            out_add = pd.concat([out_add, other[other[other.idField] == idx]])
        # 找到B表中删除的行数
        for idx in removed_rows:
            out_remove = pd.concat([out_remove, self[self[self.idField] == idx]])
        output['diffA'] = out_difA
        output['diffB'] = out_difB
        output['add'] = out_add
        output['remove'] = out_remove
        return output
class ExTable(MyDF):
    def __init__(self, path, sheetName, skipRows = [], idField = "ID"):
        super().__init__(pd.read_excel(path, sheet_name = sheetName, skiprows=skipRows))
        self.idField = idField
        self.path = path

class CSVTable(MyDF):
    def __init__(self, path, skipRows = [], idField = "---"):
        super().__init__(pd.read_csv(path, skiprows=skipRows))
        self.idField = idField
        self.path = path