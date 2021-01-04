########################################
###node类测试
########################################
#      add sfcsim path to sys path ##########
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end  
from sfcsim import *
print(node.__doc__)
vnf_types=vnf_types(5)
node1=node(atts={'cpu':10,'memory':10,'storage':10,'access':False}) 
node2=node(uuid='node2',atts={'cpu':10,'memory':10,'storage':10,'access':False})
print('*****************     测试读取数据    ******************')
print(node1.get_id(),node1.get_atts(),node1.get_vnfs(),node1.get_remain_resource(),node1.is_access(),node1.is_idle())
node1.show()
node2.show()
print('*****************     测试修改数据    ******************')
node1.set_id('node01')
node1.set_atts({'cpu':20})
node1.add_vnf(vnf_type(atts={'cpu':1,'memory':1,'storage':1}))
print(node1.get_vnfs())
node1.show()
node2.show()
node1.set_access_node()
print('*****************     测试伸缩vnf数据    ******************')
node1.add_vnf(vnf_type(atts={'cpu':1},resource_coefficient={'cpu':1}))
print(node1.get_vnfs())
node1.scale_out_vnf('vnf_type1',{'cpu':3,'memory':3,})
node1.show()
node1.scale_in_vnf('vnf_type1')
# node1.show()
node1.add_vnf(vnf_type('vnf_type2',atts={'cpu':1},resource_coefficient={'cpu':1}))
node1.scale_in_vnf('vnf_type2')
print(node1.get_atts(),node1.get_remain_resource())
node=node1
lens=len(node.get_vnfs())
for i in range(lens):
    j=lens-i-1
    if node.get_vnfs()[j].is_idle()==True:
        node.delete_vnf(node.get_vnfs()[j].get_name())
node1.show()