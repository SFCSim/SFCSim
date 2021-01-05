#mobile_sfc类测试
from sfcsim import *
print(sfc.__doc__)
vnf_types=vnf_types(5)
vnf_types.show()
sfc1=mobile_sfc('m_sfc1',['in1','in2'],'out',['vnf_type1','vnf_type2'],bandwidth=1,duration=2,vnf_types=vnf_types)
print('*****************     测试读取数据    ******************')
print(sfc1.get_id(),sfc1.get_in_node(),sfc1.get_out_node(),sfc1.get_bandwidths(),sfc1.get_duration(),\
      sfc1.get_delay(),sfc1.get_profit(),sfc1.get_length(),sfc1.get_type())
sfc1.show()
print('*****************     测试修改数据    ******************')
sfc1.set_atts({'bandwidth':2})
sfc1.set_atts({'in_nodes':['in1','in2','in3']})
sfc1.set_atts({'duration':2})
sfc1.show()
# sfc1.set_atts({'nfs':['vnf_type1']})
# sfc1.show()
print('*****************     测试输入节点移动    ******************')
for i in range(10):
    print('第 %d 个周期结束，进入第%d个周期' %(i+1,i+2))
    print('状态是否改变:',sfc1.next_cycle())
    sfc1.show()
    print('是否结束生命周期：',sfc1.is_life_end())