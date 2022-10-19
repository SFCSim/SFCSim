def deploy_sfc_node_equal_nf(self,sfc,network,shortest_path,path_delay,vnf_types):   #len(shortest_path)==sfc.get_length()-2
        if path_delay<=sfc.get_delay():                       #判断链路延迟是否满足需求
            nf_number=sfc.get_length()-2
            #*******************先部署nf****************************************
            for i in range(nf_number):                         
                if self.deploy_nf_scale_out(sfc,shortest_path[i],i+1,vnf_types)!=True:
                    for j in range(i):                          #部署失败则把之前的部署都清空
                        self.remove_nf(sfc,j+1)
                    if self.log==True:
                        print('log:  can\'t deploy nf %d in %s on %s' %(i+1,sfc.get_id(),shortest_path[i+1].get_id()))
                    return False
            #*******************部署虚拟链路****************************************
            for i in range(nf_number+1):                          
                if i==0:
                    if self.deploy_link(sfc,1,network,[shortest_path[0],shortest_path[0]])!=True:
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link 1 in %s on %s-%s' %(sfc.get_id(),shortest_path[0].get_id(),shortest_path[0].get_id()))
                        return  False
                elif i==nf_number:
                    if self.deploy_link(sfc,i+1,network,[shortest_path[i-1],shortest_path[i-1]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1].get_id(),shortest_path[i-1].get_id()))
                        return  False
                else :
                    if self.deploy_link(sfc,i+1,network,[shortest_path[i-1],shortest_path[i]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1].get_id(),shortest_path[i].get_id()))
                        return  False
            return True
        else:
            if self.log==True:
                print('log:  can\'t deploy sfc:%s, path delay %s > sfc delay %s' %(sfc.get_id,path_delay,sfc.get_delay()))
            return False
        return True
    def deploy_sfc_node_more_than_nf(self,sfc,network,shortest_path,path_delay,vnf_types):   #len(shortest_path)>sfc.get_length()-2
        if path_delay<=sfc.get_delay():                       #判断链路延迟是否满足需求
            nf_number=sfc.get_length()-2
            node_number=len(shortest_path)
            dup=node_number-nf_number              #第dup条路径需要重复部署次数
            index=np.argmin(sfc.get_bandwidths())   #第index条虚拟链路需要重复部署dup次
            #*******************先部署nf****************************************
            for i in range(nf_number):                          
                if i<index:
                    if self.deploy_nf_scale_out(sfc,shortest_path[i],i+1,vnf_types)!=True:  #index之前的nf按顺序部署
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy nf %d in %s on %s' %(i+1,sfc.get_id(),shortest_path[i].get_id())) 
                        return False
                else :
                    if self.deploy_nf_scale_out(sfc,shortest_path[i+dup],i+1,vnf_types)!=True: #index之后的nf跳过dup个node顺序部署
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy nf %d in %s on %s' %(i+1,sfc.get_id(),shortest_path[i+dup].get_id())) 
                        return False
            #*******************部署虚拟链路****************************************
            for i in range(nf_number+1):                          
                if i==0 :                          #虚拟链路首节点为输入节点，需要特殊部署
                    if i == index:
                        if self.deploy_link(sfc,1,network,shortest_path[0:i+dup+1])!=True:
                            for j in range(nf_number):                          #部署失败则把之前的部署都清空
                                self.remove_nf(sfc,j+1)
                            if self.log==True:
                                print('log:  can\'t deploy link 1 in %s on %s-%s' %(sfc.get_id(),shortest_path[0].get_id(),shortest_path[i+dup].get_id()))
                            return  False  
                    else:
                        if self.deploy_link(sfc,1,network,[shortest_path[0],shortest_path[0]])!=True:
                            for j in range(nf_number):                          #部署失败则把之前的部署都清空
                                self.remove_nf(sfc,j+1)
                            if self.log==True:
                                print('log:  can\'t deploy link 1 in %s on %s-%s' %(sfc.get_id(),shortest_path[0].get_id(),shortest_path[0].get_id()))
                            return  False       
                elif i==nf_number:                #虚拟链路尾节点为输出节点，需要特殊部署
                    if i == index:
                        if self.deploy_link(sfc,i+1,network,shortest_path[index-1:node_number])!=True:
                            for j in range(i):                          #部署失败则把之前的部署都清空
                                self.remove_link(sfc,j+1,network)
                            for j in range(nf_number):                          #部署失败则把之前的部署都清空
                                self.remove_nf(sfc,j+1)
                            if self.log==True:
                                print('log:  can\'t deploy link %d in on %s%s' %(i+1,sfc.get_id(),[shortest_path[index-1].get_id(),shortest_path[node_number-1].get_id()]))
                            return  False
                    else:
                        if self.deploy_link(sfc,i+1,network,[shortest_path[node_number-1],shortest_path[node_number-1]])!=True:
                            for j in range(i):                          #部署失败则把之前的部署都清空
                                self.remove_link(sfc,j+1,network)
                            for j in range(nf_number):                          #部署失败则把之前的部署都清空
                                self.remove_nf(sfc,j+1)
                            if self.log==True:
                                print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[node_number-1].get_id(),shortest_path[node_number-1].get_id()))
                            return  False 
                elif i<index :                     #最短代价虚拟链路之前的虚拟链路部署方案
                    if self.deploy_link(sfc,i+1,network,[shortest_path[i-1],shortest_path[i]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1) 
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1].get_id(),shortest_path[i].get_id()))  
                        return False
                elif i==index :                    #最短代价虚拟链路部署方案
                    if self.deploy_link(sfc,i+1,network,shortest_path[i-1:i+dup+1])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)  
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1].get_id(),shortest_path[i+dup].get_id()))  
                        return False
                else :                              #最短代价虚拟链路之后的虚拟链路部署方案
                    if self.deploy_link(sfc,i+1,network,[shortest_path[i-1+dup],shortest_path[i+dup]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1) 
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1+dup].get_id(),shortest_path[i+dup].get_id()))  
                        return False
            return True
        else:
            if self.log==True:
                print('log:  can\'t deploy sfc:%s, path delay %s > sfc delay %s' %(sfc.get_id(),path_delay,sfc.get_delay()))
            return False
    def deploy_sfc_node_less_than_nf(self,sfc,network,shortest_path,path_delay,vnf_types):   #len(shortest_path)<sfc.get_length()-2
        if path_delay<=sfc.get_delay():                       #判断链路延迟是否满足需求
            nf_number=sfc.get_length()-2
            node_number=len(shortest_path)
            dup=nf_number-node_number               #多余dup个nf需要部署在相同node上
            indexs=list(np.argsort(-np.array(sfc.get_bandwidths())))
            indexs.remove(0)
            indexs.remove(nf_number)
            indexs=indexs[0:dup]   #排在前面的为需求比较大的虚拟链路，其两端nf部署在同一个节点上,首尾链路不参加合并
            #*******************先部署nf****************************************
            alerady_dup=0
            for i in range(nf_number):                          
                if i in indexs:            #需要重复部署的nf
                    if self.deploy_nf_scale_out(sfc,shortest_path[i-alerady_dup-1],i+1,vnf_types)!=True:  #表示此nf与上一个nf部署在同一个节点上
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy nf%d in %s on %s' %(i+1,sfc.get_id(),shortest_path[i-alerady_dup-1].get_id())) 
                        return False
                    alerady_dup+=1
                else :
                    if self.deploy_nf_scale_out(sfc,shortest_path[i-alerady_dup],i+1,vnf_types)!=True: #
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy nf%d in %s on %s' %(i+1,sfc.get_id(),shortest_path[i-alerady_dup].get_id())) 
                        return False
            #*******************部署虚拟链路****************************************
            alerady_dup=0
            for i in range(nf_number+1):                          
                if i==0:
                    if self.deploy_link(sfc,1,network,[shortest_path[0],shortest_path[0]])!=True:
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(1,sfc.get_id(),shortest_path[0].get_id(),shortest_path[0].get_id()))  
                        return False
                elif i==nf_number:
                    if self.deploy_link(sfc,i+1,network,[shortest_path[node_number-1],shortest_path[node_number-1]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[node_number-1].get_id(),shortest_path[node_number-1].get_id())) 
                        return False
                elif i in indexs :
                    if self.deploy_link(sfc,i+1,network,[shortest_path[i-1-alerady_dup],shortest_path[i-1-alerady_dup]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1-alerady_dup].get_id(),shortest_path[i-1-alerady_dup].get_id())) 
                        return False
                    alerady_dup+=1
                else:
                    if self.deploy_link(sfc,i+1,network,[shortest_path[i-1-alerady_dup],shortest_path[i-alerady_dup]])!=True:
                        for j in range(i):                          #部署失败则把之前的部署都清空
                            self.remove_link(sfc,j+1,network)
                        for j in range(nf_number):                          #部署失败则把之前的部署都清空
                            self.remove_nf(sfc,j+1)
                        if self.log==True:
                            print('log:  can\'t deploy link %d in %s on %s-%s' %(i+1,sfc.get_id(),shortest_path[i-1-alerady_dup].get_id(),shortest_path[i-alerady_dup].get_id())) 
                        return False
            return True
        else:
            if self.log==True:
                print('log:  can\'t deploy sfc:%s, path delay %s > sfc delay %s' %(sfc.get_id(),path_delay,sfc.get_delay()))
            return False
    def bubbleSort(self,arr): #冒泡排序，先部署流量大的vnf
        n = len(arr)
        # 遍历所有数组元素
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n-i-1):
                if arr[j].get_bandwidths()[0] < arr[j+1].get_bandwidths()[0] :
                    arr[j], arr[j+1] = arr[j+1], arr[j]
    def deploy_sfc(self,network,sfc,p,delay_list,vnf_types):
        result=False
        in_node=network.get_node(sfc.get_in_node())
        out_node=network.get_node(sfc.get_out_node())
        shortest_path=p[in_node][out_node]
        path_delay=delay_list[in_node][out_node]
        if len(shortest_path) > sfc.get_length()-2:
            result= self.deploy_sfc_node_more_than_nf(sfc,network,shortest_path,path_delay,vnf_types)
        elif len(shortest_path) < sfc.get_length()-2:
            result= self.deploy_sfc_node_less_than_nf(sfc,network,shortest_path,path_delay,vnf_types)
        else:
            result= self.deploy_sfc_node_equal_nf(sfc,network,shortest_path,path_delay,vnf_types)
        if(result==True):
            self.add_sfc_record(sfc)
        else:
            if sfc.get_id() in self.__records:
                del self.__records[sfc.get_id()]
        return result
    def auto_scheduling(self,network):
        super(shortest_path_scheduler, self).auto_scheduling(network)
        for node in network.get_nodes():
            for vnf in node.get_vnfs():
                if vnf.is_idle()==True:
                    node.delete_vnf(vnf.get_name())
                else:
                    node.scale_in_vnf(vnf.get_name())
                
    def deploy_sfcs(self,network,vnf_types,sfcs,sort=True):
        if(sort==True):
            self.bubbleSort(sfcs.get_sfcs())
        p=nx.shortest_path(network.G, weight='delay')          #所有节点到所有节点的最短路径集合
        delay_list=dict(nx.shortest_path_length(network.G, weight='delay')) #所有最短路径的权值集合
        sfc_list=sfcs.get_sfcs()
        i=0
        for sfc in sfc_list:
            self.deploy_sfc(network,sfc,p,delay_list,vnf_types)