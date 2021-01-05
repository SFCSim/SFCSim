#####################################
## vnf_types类测试文件
####################################
from sfcsim import *
cernnet=cernnet2()
node_list=['node1','node2','node3','node4','node5']
edge=[[1,0,1,1,1],[0,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
edge_atts={'delay':[[1,2,3,1,1],[2,1,1,1,1],[3,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]}
network_matrix1=network_matrix(node_list,edge,edge_atts)
network_matrix1.set_edge_att('bandwidth',[[1,2,3,4,1],[2,1,1,1,1],[3,1,1,1,1],[4,1,1,1,1],[1,1,1,1,1]])
network_matrix1.show()
network_matrix1.update([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],\
                     {'bandwidth':[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]})
network_matrix1.show()
# 测试直接从network类生成网络
network_matrix2=network_matrix()
network_matrix2.generate(cernnet)
network_matrix2.show()