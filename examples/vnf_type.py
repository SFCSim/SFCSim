#####################################
###vnf_type类测试文件
####################################
#      add sfcsim path to sys path ##########
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end    
from sfcsim import *

print(vnf_type.__doc__)
vnf_type1=vnf_type('vnf_type1')
vnf_type2=vnf_type('vnf_type2')
vnf_type1.show()
vnf_type2.show()
print('*****************     测试读取数据    ******************')
print(vnf_type1.get_name(),vnf_type1.get_atts(),vnf_type1.get_ratio(),vnf_type1.get_coeff(),vnf_type1.get_remain_resource())
print(vnf_type2.get_name(),vnf_type2.get_atts(),vnf_type2.get_ratio(),vnf_type2.get_coeff(),vnf_type2.get_remain_resource())
print('*****************     测试修改数据    ******************')
vnf_type1.set_name('type')
vnf_type1.set_ratio(3)
vnf_type1.set_atts({'cpu': 10, 'memory': 20, 'storage': 30})
vnf_type1.set_coeff({'cpu': 2, 'memory': 2, 'storage': 2})
vnf_type2.set_atts({'cpu': 20})
vnf_type1.show()
vnf_type2.show()