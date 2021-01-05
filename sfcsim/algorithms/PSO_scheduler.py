import random
import numpy as np
from sfcsim.algorithms import common
import time
from sfcsim.classes import *
class PSO_scheduler(dynamic_scheduler):
    def __init__(self,pN=10,max_iter=100,w_local=0.3,w_global=0.4,log=False):   #log=means not to print deployment procedure information
        super(PSO_scheduler, self).__init__(log=log)
        self.__records=super(PSO_scheduler, self).get_records()
        # self.__records=self.get_records()
        self.w_local=w_local    #局部概率
        self.w_global=w_global   #全局概率
        self.pN=pN  # 粒子数量
        self.particles=[]     #初始化粒子群的部署方法
        self.v=[]
        self.max_iter=max_iter  # 迭代次数 
        self.pbest={}  # 个体经历的最佳位置和全局最佳位置
        self.gbest={}
        self.p_fit=[]    
        self.g_fit=[]   # 全局最佳适应值，最后一个是最新的fit，前面是每一次迭代的fit
        self.solutions_length={}
        self.all_sfc_deploy_solutions={}   #存储对所有sfc的所有可行方案,以字典格式存储{'sfc1':[{},{},{}],...}
    def show_solutions(self,sfc_id):
        print(sfc_id)
        for solution in self.all_sfc_deploy_solutions[sfc_id]:
            print('        ',solution)
 
    def show_particles(self):
        for particle in self.particles:
            for sfc_id in particle:
                print(sfc_id,particle[sfc_id])
    def sample(self,lists,num):
        lens=len(lists)
        if num<=lens:
            return random.sample(lists,num)
        else:
            lists2=[]
            for i in range(num):
                j=i%lens
                lists2.append(lists[j])
                if(i==lens-1):
                    lists2.append(-1)  #空解，表示不部署这条sfc
            return lists2

    def sample_solution(self,sfc,X=3): #X表示指数衰退因子
        sfc_id=sfc.get_id()
        solutions=self.all_sfc_deploy_solutions[sfc_id]
        lens=len(solutions)
        sample_solutions=[]
        if(lens<self.pN):
            for i in range(self.pN):
                if(lens==0):
                    sample_solutions.append(-1)  #空解，表示不部署这条sfc
                else:
                    j=i%lens
                    sample_solutions.append(j)
                    if(j==lens-1):
                        sample_solutions.append(-1)  #空解，表示不部署这条sfc
        else:
            remain=self.pN
            index1=lens
            index2=lens*2
            for i in range(X+1):
                if(i==0):
                    index1=int(index1/2)
                    index2=int(index2/2)
                    allo_number=int(self.pN/(2**(X-i))) #这一次分配的粒子数
                    # print('allo_number=>',allo_number+1)
                    remain=remain-allo_number-1  #剩余粒子数,因为加入了一个空集合
                    sample_solutions=sample_solutions+self.sample(range(index1,index2),allo_number)
                    sample_solutions.append(-1)    
                elif(i !=X):
                    index1=int(index1/2)
                    index2=int(index2/2)
                    allo_number=int(self.pN/(2**(X-i+1))) #这一次分配的粒子数
                    # print('allo_number=>',allo_number+1)
                    remain=remain-allo_number-1  #剩余粒子数,因为加入了一个空集合
                    sample_solutions=sample_solutions+self.sample(range(index1,index2),allo_number)
                    sample_solutions.append(-1)
                else:
                    # print('allo_number last=>',remain)
                    index1=0
                    index2=int(index2/2)
                    sample_solutions=sample_solutions+self.sample(range(index1,index2),remain)
        # print(sample_solutions)
        random.shuffle(sample_solutions)
        return sample_solutions

    def clear_network(self,network,sfcs):
        records_list=[]
        for sfc_id in self.get_records():    
            records_list.append(sfc_id)    #存，防止字典/列表长度随迭代变化
        for i in records_list:
            self.remove_sfc(sfcs.get_sfc(i),network)    
        for node in network.get_nodes():
            vnfs=network.get_vnfs(node.get_id())
            vnfs_list=[]
            for j in range(len(vnfs)):                   
                vnfs_list.append(vnfs[j].get_name())    
            for i in vnfs_list:                   
                network.delete_vnf(node.get_id(),i)

    def deploy_sfc_by_records(self,sfcs,network,vnf_types,records):
        for sfc_id in records:
            if records[sfc_id] !=-1:  #{}表示不部署这条sfc
                log=True
                sfc=sfcs.get_sfc(sfc_id)
                for i in records[sfc_id]['node']:
                    if self.deploy_nf_scale_out(sfc,network.get_node(records[sfc_id]['node'][i]),i,vnf_types)!=True:   
                        if sfc_id in self.get_records(): 
                            self.remove_sfc(sfc,network) 
                        log=False
                    if log==False:
                        break      #跳出1层循环
                if log==False:   #这条条sfc部署失败，执行下一条sfc的部署 
                    continue    
                for j in records[sfc_id]['edge']: 
                    edge_list=records[sfc_id]['edge'][j]
                    edge=[]
                    for m in range(len(edge_list)):
                        edge.append(network.get_node(edge_list[m]))
                    if self.deploy_link(sfc,j,network,edge)!=True:  #链路部署失败，则将sfc删除
                        if sfc.get_id() in self.get_records():
                            self.remove_sfc(sfc,network)   
                        log=False                  
                    if log==False:
                        break    #跳出1层循环
        fit=0
        record=self.get_records()
        for sfc_id in record:    #所有sfc的虚拟链路相加之和
            if 'node' in record[sfc_id] and 'edge' in record[sfc_id]:
                if len(record[sfc_id]['node'])== sfcs.get_length(sfc_id)-2 and len(record[sfc_id]['edge'])== sfcs.get_length(sfc_id)-1:
                    for bandwidth in sfcs.get_bandwidths(sfc_id):
                        fit=fit+bandwidth
        self.clear_network(network,sfcs)            
        return fit 
    def get_deploy_solution_from_particle(self,particle):
        record={}
        for sfc_id in particle: 
            if particle[sfc_id] !=-1:
                record[sfc_id]={'node':{},'edge':{}}
                solution=self.all_sfc_deploy_solutions[sfc_id][particle[sfc_id]]
                for i in solution['node']:
                    record[sfc_id]['node'][i]=solution['node'][i]
                for j in solution['edge']:
                    record[sfc_id]['edge'][j]=solution['edge'][j]
            else:
                record[sfc_id]=-1
        return record
    def calculate_fit(self,sfcs,network,vnf_types,particle):    #计算单粒子fit  
        records=self.get_deploy_solution_from_particle(particle)
        return self.deploy_sfc_by_records(sfcs,network,vnf_types,records)
    def init_particle(self,network,sfcs,vnf_types,n):    #初始化粒子群，最优解，fit \
        mode,self.all_sfc_deploy_solutions=common.find_sfcs_solutions(network,sfcs,n)   #先找到所有可行的部署方案 
        for sfc_id in self.all_sfc_deploy_solutions:
            self.solutions_length[sfc_id]=len(self.all_sfc_deploy_solutions[sfc_id])
        ####### 初始化粒子 self.particle
        for i in range(self.pN):
            self.particles.append({})
            self.v.append({})
        for sfc in sfcs.get_sfcs():
            solutions=self.sample_solution(sfc)
            for i in range(self.pN):
                self.particles[i][sfc.get_id()]=solutions[i]
                self.v[i][sfc.get_id()]=0
        ####### 初始化粒子适应度 
        for particle in self.particles:    #初始化粒子fit
            self.p_fit.append(self.calculate_fit(sfcs,network,vnf_types,particle))
        ####### 初始化粒子最佳位置
        self.pbest=copy.deepcopy(self.particles)   #粒子局部最优解
        best_fit=max(self.p_fit)            #本次粒子全局最优适应度
        self.g_fit.append(best_fit)           
        self.gbest=copy.deepcopy(self.particles[self.p_fit.index(best_fit)]) ####粒子全局最优解
                 
    def update(self,sfcs,network,vnf_types,index):    #更新全部粒子
        lens=len(self.particles[index])
        g_rand=np.random.random(lens)*self.w_global
        p_rand=np.random.random(lens)*self.w_local
        i=0
        for sfc_id in self.particles[index]:
            if self.particles[index][sfc_id] !=-1:   #-1表示不部署，则一直保持-1
                self.v[index][sfc_id]=self.v[index][sfc_id]+\
                                            p_rand[i]*self.solutions_length[sfc_id]*(self.pbest[index][sfc_id]-self.particles[index][sfc_id])+\
                                            g_rand[i]*self.solutions_length[sfc_id]*(self.gbest[sfc_id]-self.particles[index][sfc_id])
                if(self.solutions_length[sfc_id]<10):
                    if(self.v[index][sfc_id]>1):
                        self.v[index][sfc_id]=1
                    elif(self.v[index][sfc_id]<-1):
                        self.v[index][sfc_id]=-1 
                else:                            
                    if(self.v[index][sfc_id]>5):
                        self.v[index][sfc_id]=5
                    elif(self.v[index][sfc_id]<-5):
                        self.v[index][sfc_id]=-5 
                self.particles[index][sfc_id]=int(round(self.particles[index][sfc_id]+self.v[index][sfc_id]))
                if self.particles[index][sfc_id]<0:
                    self.particles[index][sfc_id]=0
                elif self.particles[index][sfc_id]>=self.solutions_length[sfc_id]:
                    self.particles[index][sfc_id]=self.solutions_length[sfc_id]-1
            # i=i+1
            
    def update_pbest(self,fit,index):    #更新单粒子pbest
        if fit>self.p_fit[index]:
            self.p_fit[index]=fit
            self.pbest[index]=copy.deepcopy(self.particles[index])       
    def update_gbest(self):      #更新gbest     
        best_fit=max(self.p_fit)            #本次粒子全局最优适应度
        index=self.p_fit.index(best_fit)          
        if best_fit>self.g_fit[-1]:
            self.g_fit.append(best_fit)    #添加更新的fit
            self.gbest=copy.deepcopy(self.particles[index])
        else:
            self.g_fit.append(self.g_fit[-1])

    def deploy_sfcs(self,sfcs,network,vnf_types,n=1):      
        # print('***********开始初始化粒子,总 %s 个***********' %(self.pN))
        start = time.clock()
        self.init_particle(network,sfcs,vnf_types,n)
        count=0
        # for i in range(100):
        #     print(pso_scheduler.particles[i])
        for s in range(self.max_iter):
            print('***********开始第 %s 次迭代***********' %(s))
            for index in range(self.pN):
                self.clear_network(network,sfcs)
                self.update(sfcs,network,vnf_types,index)    #更新粒子
                fit=self.calculate_fit(sfcs,network,vnf_types,self.particles[index])    #计算fit
                self.update_pbest(fit,index)    #更新个体最优
            self.update_gbest()    #更新全局最优
            if abs(self.g_fit[-1]-self.g_fit[len(self.g_fit)-2])<0.0001  :
                count+=1
            else:
                count=0
            if count==1000:
                break
            else:
                end = time.clock()
                print('time=>',end-start,'s','max grade=>',self.g_fit[-1])
        print('***********迭代已完成***********')
        #—————最终部署按gbest部署sfcs——————
        end = time.clock()
        print('time=>',end-start,'s',self.g_fit)




