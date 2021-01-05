from sfcsim.classes import *
from sfcsim.algorithms import common
import time
class TS_scheduler(dynamic_scheduler):
    def __init__(self,tabu_length=10,iteration=50,stop_condition=5,log=False):   #log=means not to print deployment procedure information
        super(TS_scheduler, self).__init__(log=log)
        self.tabu_list=[]
        self.tabu_length=tabu_length          
        self.stop_condition=stop_condition
        self.iteraction_count=iteration       #最大迭代次数

        self.max_deploy_record={}          #存储最优解的解量
        self.max_deploy_solution={}        #存储最优解的数字量
        self.global_max_deploy_record={}        #存储全局最优解记录
        self.grade_list=[]       #存储所有迭代的最优分数
        ###############################################
        self.all_sfc_deploy_solutions={}   #存储对所有sfc的所有可行方案,以字典格式存储{'sfc1':[{},{},{}],...}
        self.solutions_length={}  #存储所有sfc的所有可能部署方案个数
        self.last_num=0   #邻域变化之前的解
   
   #清除网络的所有sfc、vnf部署，同时清空记录
    def clear_network(self,network,sfcs): 
        records_list=[]
        for sfc_id in self.get_records():    
            records_list.append(sfc_id)    #存储key，防止字典/列表长度随迭代变化
        for i in records_list:
            self.remove_sfc(sfcs.get_sfc(i),network)    
        for node in network.get_nodes():
            vnfs=network.get_vnfs(node.get_id())
            vnfs_list=[]
            for j in range(len(vnfs)):                   
                vnfs_list.append(vnfs[j].get_name())    
            for i in vnfs_list:                   
                network.delete_vnf(node.get_id(),i)

    #检查服务的总流量大小
    def check_score(self,record,sfcs): 
        grade=0
        for sfc_id in record:
            if 'node' in record[sfc_id] and 'edge' in record[sfc_id]:
                if len(record[sfc_id]['node'])== sfcs.get_length(sfc_id)-2 and len(record[sfc_id]['edge'])== sfcs.get_length(sfc_id)-1:
                    for bandwidth in sfcs.get_bandwidths(sfc_id):
                        grade=grade+bandwidth
        return grade
    
    #通过记录执行部署操作并计算返回适应度
    def deploy_sfc_by_records(self,sfcs,network,vnf_types,records):#通过记录部署所有服务功能链
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
    
    #获得进行邻域操作之后的新部署方案 
    def get_new_deploy_solution(self,neighbour):
        self.last_num=copy.deepcopy(self.max_deploy_solution[neighbour[0]])
        if neighbour[1] !=0:
            self.max_deploy_solution[neighbour[0]]+=neighbour[1]
            self.max_deploy_record[neighbour[0]]=self.all_sfc_deploy_records[neighbour[0]][self.max_deploy_solution[neighbour[0]]]
        else:
            self.max_deploy_solution[neighbour[0]]=-1
            self.max_deploy_record[neighbour[0]]=-1

    #回到邻域操作之前的部署方案   
    def get_last_deploy_solution(self,neighbour):
        self.max_deploy_solution[neighbour[0]]=self.last_num
        if self.last_num!=-1:
            self.max_deploy_record[neighbour[0]]=self.all_sfc_deploy_records[neighbour[0]][self.max_deploy_solution[neighbour[0]]]
        else:
            self.max_deploy_record[neighbour[0]]=-1
    
    # 获得一条sfc的部署邻域
    def get_neighbour(self,sfc_id):
        neighbour=[]
        num=self.max_deploy_solution[sfc_id]
        max_num=self.solutions_length[sfc_id] #获得最大id
        if num>0 :
            neighbour.append((sfc_id,-1))
        if num<max_num-1:
            neighbour.append((sfc_id,1))
        if num!=-1:
            neighbour.append((sfc_id,0))      #0表示不部署这条sfc
        # print('neighbour=>',neighbour)
        return neighbour

    # 获得单前解的所有邻域
    def get_neighbours(self):
        neighbours=[]
        for sfc_id in self.max_deploy_record:
            neighbours.extend(self.get_neighbour(sfc_id))
        return neighbours

    #判断邻域是否在禁忌表中
    def is_in_tabu_list(self,neighbour):   #判断邻域是否在禁忌列表中
        lens=len(self.tabu_list) 
        for data in self.tabu_list:
            if data[0]== neighbour[0] and data[1] == -neighbour[1]:  #
                return True
        return False

    #计算邻域的适应度
    def calculate_fits(self,sfcs,network,vnf_types,neighbours):   
        fits=[]
        for neighbour in neighbours: 
            self.get_new_deploy_solution(neighbour)         #进入新领域
            fits.append(self.deploy_sfc_by_records(sfcs,network,vnf_types,self.max_deploy_record))
            self.get_last_deploy_solution(neighbour)        #回退到原始最优解
        return fits

     #执行一次搜索
    def single_search(self,network,sfcs,vnf_types):   
        neighbours=self.get_neighbours()  #获得解集合和对应邻域操作  neighbours=[('sfc1',1),('sfc2',1),...]
        # print('neighbours=>',neighbours)
        fits=self.calculate_fits(sfcs,network,vnf_types,neighbours)    #计算所有邻域的适应度
        candidate_grade=max(fits)                           #获取最大适应度
        neighbour=neighbours[fits.index(candidate_grade)]    #获取最大适应度所在邻域

        if candidate_grade > self.max_grade:          #藐视法则
            print('************  new solution***********')
            self.max_grade = candidate_grade
            if self.is_in_tabu_list(neighbour):                            
               self.tabu_list.remove(neighbour)
            self.tabu_list.append(neighbour)
            if len(self.tabu_list) > self.tabu_length:                  #判断该禁忌列表长度是否以达到限制，是的话移除最初始的move
               self.tabu_list.remove(self.tabu_list[0])
            self.get_new_deploy_solution(neighbour)   
            self.global_max_deploy_record=copy.deepcopy(self.max_deploy_record)
            return True
        else:
            print('************ old solution***********')
            while(self.is_in_tabu_list(neighbour)):
                fits[fits.index(candidate_grade)]=-1   #把最优解设置为最小值 
                candidate_grade=max(fits) 
                neighbour=neighbours[fits.index(candidate_grade)]    #获取最大适应度所在邻域
            self.tabu_list.append(neighbour)
            if len(self.tabu_list) > self.tabu_length:                  #判断该禁忌列表长度是否以达到限制，是的话移除最初始的move
               self.tabu_list.remove(self.tabu_list[0])
            self.get_new_deploy_solution(neighbour)                           #更新最优解
            return False

    #初始化，提前计算一些常用的量
    def init(self,init_record,network,sfcs):    
        self._scheduler__records=init_record
        self._dynamic_scheduler__records=init_record
        self.__records=self.get_records()     #更新初始解
        self.max_grade=self.check_score(init_record,sfcs)                     #更新初始目标值
        self.all_sfc_deploy_solutions,self.all_sfc_deploy_records=common.find_sfcs_solutions(network,sfcs,1)   #先找到所有可行解的部署方案，第一项是数字记录，第二项为字符串记录
        for sfc_id in self.all_sfc_deploy_solutions:  #每一条sfc的部署方案
            self.solutions_length[sfc_id]=len(self.all_sfc_deploy_solutions[sfc_id])
        self.max_deploy_record=common.records_node_to_str(self.get_records())         #存储最优解的字符串量
        for sfc_id in self.all_sfc_deploy_records:
            if sfc_id not in self.max_deploy_record:
                self.max_deploy_record[sfc_id]=-1
        self.max_deploy_solution=common.records_str_to_num(self.max_deploy_record,self.all_sfc_deploy_records)       
        self.clear_network(network,sfcs)

    #主函数
    def deploy_sfcs(self,network,sfcs,vnf_types,init_record):  
        start = time.clock()
        self.init(init_record,network,sfcs)
        for i in range(self.iteraction_count):
            if self.single_search(network,sfcs,vnf_types)==True:  #进行一轮搜索
                count=0
            else:
                count=count+1
            self.grade_list.append(self.max_grade)
            end = time.clock()
            print('time=>',end-start,'s','max grade=>',self.max_grade)
            if(count>self.stop_condition):
                print("迭代%d次为发现更优解，迭代停止"%(self.stop_condition))
                break
        end = time.clock()
        print('execution time=>',end-start,'s')
        print('optimal solution=>',self.max_grade,'  =>',self.global_max_deploy_record)







