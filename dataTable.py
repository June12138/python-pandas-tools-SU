import pandas as pd

class MyDF(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idField = None
        self.path = None
    @classmethod
    def from_excel(cls, path, sheet_name, skipRows=None, idField="ID", dtype=str):
        # 读取Excel
        df = pd.read_excel(path, sheet_name=sheet_name, skiprows=skipRows, dtype=dtype)
        # 创建MyDF实例
        instance = cls(df)
        instance.idField = idField
        instance.path = path
        return instance
    @classmethod
    def from_csv(cls, path, skipRows=None, idField="---", dtype=str):
        # 读取CSV
        df = pd.read_csv(path, skiprows=skipRows, dtype=dtype)
        instance = cls(df)
        instance.idField = idField
        instance.path = path
        return instance
    def GetRowByID(self, id):
        return self[self[self.idField] == id]
    def QuickSearch(self, searchField, searchKey, returnKey):
        return self[self[searchField] == searchKey].iloc[0][returnKey]
    def SearchContain(self, searchField, searchKey, returnKey):
        for i in range(0, len(self)):
            currentRow = self.iloc[i]
            if searchKey in str(currentRow[searchField]):
                return currentRow[returnKey]
    def Compare(self, other):
        output = {}
        # Find common, added, and removed rows
        selfIDList = []
        otherIDList = []
        for i in range(0,len(self)):
            selfIDList.append(self.iloc[i][self.idField])
        for i in range(0,len(other)):
            otherIDList.append(other.iloc[i][self.idField])
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

        # Initialize output DataFrames
        out_difA = MyDF(pd.DataFrame(columns=self.columns))
        out_difB = MyDF(pd.DataFrame(columns=other.columns))
        out_add = MyDF(pd.DataFrame(columns=other.columns))
        out_remove = MyDF(pd.DataFrame(columns=self.columns))
        out_difA['_diff_cols'] = pd.Series(dtype=object)
        out_difB['_diff_cols'] = pd.Series(dtype=object)

        # Find differing rows
        for i in common_ids:
            self_row = self[self[self.idField] == i].copy()  # Create a copy to avoid SettingWithCopyWarning
            other_row = other[other[other.idField] == i].copy()
            diff_cols = []
            for col in self_row.columns:
                if col == self.idField:
                    continue
                val1, val2 = None, None
                try:
                    val1, val2 = self_row[col].iloc[0], other_row[col].iloc[0]
                except:
                    pass
                if pd.isna(val1) and pd.isna(val2):
                    continue
                if val1 != val2:
                    diff_cols.append(col)
            if diff_cols:
                try:
                    self_row['_diff_cols'] = [diff_cols]
                    other_row['_diff_cols'] = [diff_cols]
                    out_difA = pd.concat([out_difA, self_row], ignore_index=True)
                    out_difB = pd.concat([out_difB, other_row], ignore_index=True)
                except:
                    print('check duplicated ID in: ' + self_row['ID'])
                    print([diff_cols])
                    print()

        # Find added rows
        for idx in added_rows:
            out_add = pd.concat([out_add, other[other[other.idField] == idx]], ignore_index=True)

        # Find removed rows
        for idx in removed_rows:
            out_remove = pd.concat([out_remove, self[self[self.idField] == idx]], ignore_index=True)

        output['diffA'] = out_difA
        output['diffB'] = out_difB
        output['add'] = out_add
        output['remove'] = out_remove
        return output
