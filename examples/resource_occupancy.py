####################################
#dynamic_scheduler类资源占用测试
####################################
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end    
from sfcsim import *
scheduler=dynamic_scheduler()
node1=node(uuid='node1',atts={'cpu':10,'memory':10,'storage':10,'access':False})
node2=node(uuid='node2',atts={'cpu':10,'memory':10,'storage':10,'access':False})
node3=node(uuid='node3',atts={'cpu':10,'memory':10,'storage':10,'access':False})
node4=node(uuid='node4',atts={'cpu':10,'memory':10,'storage':10,'access':False})
node5=node(uuid='node5',atts={'cpu':10,'memory':10,'storage':10,'access':False})
print('*****************     生成vnf_types    ******************')
vnf_types=vnf_types(3)
vnf_types.set_ratio('vnf_type1',2)
vnf_types.set_coeff('vnf_type2',{'cpu': 2})
vnf_types.show()
print('*****************     生成测试网络    ******************')   
network=network([node1,node2,node3,node4,node5])
network.add_edges([['node1',node2,{'bandwidth':10}],['node1',node3,{'bandwidth':20,'delay':10}],\
                   ['node2',node3,{'bandwidth':10}],['node2','node4',{'bandwidth':10}],['node5','node4',{'bandwidth':10}]])
network.add_vnf('node1',vnf_type(name='vnf_type1',atts={'cpu':2,'memory':2,'storage':2}))
network.add_vnf('node1',vnf_type(name='vnf_type2',atts={'cpu':2,'memory':2,'storage':2}))
network.add_vnf('node2',vnf_type(name='vnf_type1',atts={'cpu':2,'memory':2,'storage':2}))
network.add_vnf('node2',vnf_type(name='vnf_type2',atts={'cpu':4,'memory':4,'storage':4}))
network.add_vnf('node3',vnf_type(atts={'cpu':1,'memory':1,'storage':1}))
print('**************************原始网络*********************************')
network.show()
print('**************************占用节点资源**********************************')
scheduler.occupy_node(network,'node1',atts={'cpu':1},time=2)
scheduler.occupy_node(network,'node1','vnf_type1',atts={'cpu':2,'memory':1},time=1)
print('**************************占用链路资源**********************************')
scheduler.occupy_edge(network,['node2','node3'],{'bandwidth':5.5},1)
scheduler.occupy_edge(network,['node2','node4','node5'],{'bandwidth':1},2)
scheduler.show_occupy_records()
network.show()
print('**************************第二个周期开始**********************************')
scheduler.auto_scheduling(network) #第二个周期
print('T=>',scheduler.T)
scheduler.show_occupy_records()
network.show()
print('**************************第三个周期开始**********************************')
scheduler.auto_scheduling(network) #第上个周期
print('T=>',scheduler.T)
scheduler.show_occupy_records()
network.show()
plt.figure(figsize=[20,15])
network.draw(nx.shell_layout(network.G))