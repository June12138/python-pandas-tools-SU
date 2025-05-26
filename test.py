from dataTable import *
import os
A = ExTable('TestData/A.xlsx', 'Sheet1', skipRows=[1])
B = ExTable('TestData/B.xlsx', 'Sheet1', skipRows=[1])

os.system('cls')
diff = A.Compare(B)
print(diff['diffA'])
print(diff['diffB'])
print(diff['add'])
print(diff['remove'])