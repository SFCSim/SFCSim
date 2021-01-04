################################
###sfc类测试
################################
#      add sfcsim path to sys path ##########
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end    
from sfcsim import *
print(sfc.__doc__)
vnf_types=vnf_types(5)
vnf_types.set_ratio('vnf_type1',3)
vnf_types.set_coeff('vnf_type2',{'cpu': 10})
vnf_types.show()
sfc1=sfc(1,'in','out',['vnf_type1','vnf_type2'],bandwidth=1,vnf_types=vnf_types)
print('*****************     测试读取数据    ******************')
print(sfc1.get_id(),sfc1.get_in_node(),sfc1.get_out_node(),sfc1.get_bandwidths(),sfc1.get_duration(),\
      sfc1.get_delay(),sfc1.get_profit(),sfc1.get_length(),sfc1.get_atts(),\
      sfc1.get_vnf_types(),sfc1.get_nfs(),sfc1.get_nfs_detail(),sfc1.get_type())
sfc1.show()
print('*****************     测试修改数据    ******************')
sfc1.set_atts({'in_node':'input','bandwidth':2,'delay':10,'duration':10,'profit':100,'nfs_detail':[]})
sfc1.show()
sfc1.set_atts({'nfs':['vnf_type1']})
sfc1.show()
print('*****************     测试多条链    ******************')
sfc2=sfc(2,'in','out',['vnf_type1','vnf_type2','vnf_type3'],bandwidth=1)
sfc2.show()
sfc2.set_vnf_types(vnf_types)
sfc2.show()