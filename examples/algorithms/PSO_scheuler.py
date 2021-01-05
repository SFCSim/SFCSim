
#####################################
## PSO_scheduler类测试文件
####################################      
from sfcsim import *
cernnet=cernnet2()                      
pso_scheduler=PSO_scheduler(pN=60,max_iter=50,w_local=0.1,w_global=0.2)
pso_scheduler.deploy_sfcs(cernnet.sfcs,cernnet,cernnet.vnf_types,n=1) 
# print(pso_scheduler.p_fit)

