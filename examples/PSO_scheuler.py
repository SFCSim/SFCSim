
#####################################
## PSO_scheduler类测试文件
####################################
#      add sfcsim path to sys path ##########
import sys     
import os
path=format(os.getcwd())
sys.path.append(path) 
# end    
from sfcsim import *
cernnet=cernnet2()                      
pso_scheduler=PSO_scheduler(pN=100,max_iter=50,w_local=0.1,w_global=0.1)
pso_scheduler.deploy_sfcs(cernnet.sfcs,cernnet,cernnet.vnf_types,n=1) 
# print(pso_scheduler.p_fit)

