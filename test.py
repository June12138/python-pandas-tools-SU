from dataTable import *
A = ExTable('TestData/A.xlsx', 'Sheet1', skipRows=[1])
B = ExTable('TestData/B.xlsx', 'Sheet1', skipRows=[1])

print(A.Compare(B))