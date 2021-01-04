
#####################################
## network_matrixs类测试
####################################
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end    
from sfcsim import *
node_list=['node1','node2','node3','node4','node5']
edge=[[1,0,1,1,1],[0,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
edge_atts={'delay':[[1,2,3,1,1],[2,1,1,1,1],[3,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]}
network_matrix1=network_matrix(node_list,edge,edge_atts)
edge=[[1,0,0,1,1],[0,1,1,1,1],[0,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
network_matrix2=network_matrix(node_list,edge,edge_atts)
edge=[[1,0,0,0,1],[0,1,1,1,1],[0,1,1,1,1],[0,1,1,1,1],[1,1,1,1,1]]
network_matrix3=network_matrix(node_list,edge,edge_atts)
network_matrixs=network_matrixs([network_matrix1,network_matrix2,network_matrix3],[1,2,3])
network_matrixs.show()
for i in range(6):
    print('******** period %d ********' %(i+1))
    data=network_matrixs.get_network_matrix(i+1)
    data.show()