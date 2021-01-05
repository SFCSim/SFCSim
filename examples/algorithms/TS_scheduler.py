# import sys     
# import os
# path=format(os.getcwd())
# sys.path.append(path) 
# # end      
from sfcsim import *

cernnet=cernnet2()          #实例化
scheduler_shortest=shortest_path_scheduler()
scheduler_shortest.deploy_sfcs(cernnet,cernnet.vnf_types,cernnet.sfcs)

#scheduler_shortest.show()
tabu=TS_scheduler(10,30)    #初始化
tabu.deploy_sfcs(cernnet,cernnet.sfcs,cernnet.vnf_types,scheduler_shortest.get_records())