#####################################
## sfcs类测试文件
####################################
#      add sfcsim path to sys path ##########
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end   
from sfcsim import *
print(sfcs.__doc__)
vnf_types=vnf_types(5)
vnf_types.set_ratio('vnf_type1',3)
vnf_types.set_coeff('vnf_type2',{'cpu': 10})
vnf_types.show()
sfc1=sfc(1,'in','out',['vnf_type1','vnf_type2'],bandwidth=1,vnf_types=vnf_types)
sfc2=sfc('sfc2','in','out',['vnf_type1','vnf_type2'],bandwidth=1,vnf_types=vnf_types)
sfc3=sfc(3,'in','out',['vnf_type1','vnf_type2','vnf_type3','vnf_type4'],bandwidth=1,vnf_types=vnf_types)
sfcs=sfcs()
sfcs.add_sfc(sfc1)
sfcs.add_sfc(sfc2)
sfcs.add_sfc(sfc3)
sfcs.show()
print('*****************     测试读取数据    ******************')
print(sfcs.get_in_node(1),sfcs.get_out_node(1),sfcs.get_bandwidths(1),sfcs.get_duration(1),\
      sfcs.get_delay(1),sfcs.get_profit(1),sfcs.get_length(1),sfcs.get_atts(1),\
      sfcs.get_vnf_types(1),sfcs.get_nfs(1),sfcs.get_nfs_detail(1),sfcs.get_type(1))
print('*****************     测试修改数据    ******************')
sfcs.set_atts(1,{'in_node':'input','bandwidth':2,'delay':10,'duration':10,'profit':100,'nfs_detail':[]})
sfcs.set_atts(1,{'nfs':['vnf_type1','vnf_type2','vnf_type3','vnf_type4','vnf_type5']})
sfcs.get_sfcs()[sfcs.search_sfc(1)].set_id('sfc1')
sfcs.show_detail()
print('*****************     测试sfc整条链    ******************')
sfcs.add_sfc(sfc1)
sfcs.add_sfc(sfc2)
sfcs.delete_sfc(3)
sfcs.add_sfc(sfc3)
print(sfcs.pop_sfc('sfc2'))
sfcs.show()