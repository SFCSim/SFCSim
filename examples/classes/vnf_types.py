#####################################
## vnf_types类测试文件
####################################
 
from sfcsim import *
print(vnf_types.__doc__)
vnf_types=vnf_types(5)
vnf_types.show()
print('*****************     测试读取数据    ******************')
print(vnf_types.get_number(),vnf_types.get_vnf_type('vnf_type1'),vnf_types.get_vnf_type('vnf_type10'),vnf_types.get_ratio('vnf_type1'),vnf_types.get_coeff('vnf_type1'))
print('*****************     测试修改数据    ******************')
vnf_types.add_vnf_type(vnf_type('vnf_type1'))
vnf_types.add_vnf_type(vnf_type('vnf_type6'))
vnf_types.show()
vnf_types.delete_vnf_type('vnf_type5')
vnf_types.delete_vnf_type('vnf_type7')
vnf_types.delete_vnf_types(['vnf_type6','vnf_type5','vnf_type4'])
vnf_types.show()
vnf_types.set_ratio('vnf_type1',3)
vnf_types.set_coeff('vnf_type2',{'cpu': 10})
vnf_types.show()