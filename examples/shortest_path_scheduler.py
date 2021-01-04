#shortest_path_scheduler类测试
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end    
from sfcsim import *
def check_score(record,sfcs): #检查服务的总流量大小
    grade=0
    for sfc_id in record:
        if 'node' in record[sfc_id] and 'edge' in record[sfc_id]:
            if len(record[sfc_id]['node'])== sfcs.get_length(sfc_id)-2 and len(record[sfc_id]['edge'])== sfcs.get_length(sfc_id)-1:
                for bandwidth in sfcs.get_bandwidths(sfc_id):
                    grade=grade+bandwidth
    return grade
    
cernnet=cernnet2()          #实例化
scheduler=shortest_path_scheduler()
scheduler.deploy_sfcs(cernnet,cernnet.vnf_types,cernnet.sfcs,sort=True)  #deploy_sfc(self,network,sfc,p,delay_list,vnf_types):
# scheduler.remove_sfc(cernnet.sfcs.get_sfc('sfc30'),cernnet)
# scheduler.deploy_sfcs_with_draw(cernnet,cernnet.vnf_types,cernnet.sfcs,path='C:/Users/86153/Desktop/fig_sort',sort=True)
#scheduler.deploy_sfcs_with_draw(cernnet,cernnet.vnf_types,cernnet.sfcs,path='C:/Users/86153/Desktop/fig',sort=False)
print('**************************************************************************')
print('you get grade=>',check_score(scheduler.get_records(),cernnet.sfcs))

# scheduler.deploy_sfc(cernnet,cernnet.sfcs.get_sfc('sfc30'),{cernnet.node4:{cernnet.node20:[cernnet.node4,cernnet.node3,cernnet.node5,cernnet.node6,cernnet.node8,cernnet.node12,\
#     cernnet.node13,cernnet.node15,cernnet.node20]}},{cernnet.node4:{cernnet.node20:0.1}},cernnet.vnf_types) #deploy_sfc(self,network,sfc,p,delay_list,vnf_types):
scheduler.show()
print(len(scheduler.get_records()))
cernnet.draw_dynamic(path='D:/1.png')
# cernnet.draw()
