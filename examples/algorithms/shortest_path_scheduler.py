#####################################
## shortest_path_scheduler类测试 
####################################  
# #      add sfcsim path to sys path ##########
# import sys     
# import os
# path=format(os.getcwd())
# sys.path.append(path) 
# # end      
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
scheduler=shortest_path_scheduler(log=True)
scheduler.deploy_sfcs_with_draw(cernnet,cernnet.vnf_types,cernnet.sfcs,sort=True,period=0.1)  #
# scheduler.deploy_sfcs(cernnet,cernnet.vnf_types,cernnet.sfcs,sort=True)
print('**************************************************************************')
print('you get grade=>',check_score(scheduler.get_records(),cernnet.sfcs))

scheduler.show()
print('deploy sfc number:',len(scheduler.get_records()))
# cernnet.draw(path='D:/1.png')
