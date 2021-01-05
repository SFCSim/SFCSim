import copy
from sfcsim.classes.network import *
class scheduler():
    '''
    scheduler类,调度器类，提供基础的调度记录功能,详情见network基础类设计文档
    属性值：
        __record             记录sfc虚拟nf和虚拟链路的部署情况
    属性方法：
        get_record
        depoly_nf
        remove_nf
        deploy_link
        remove_link
    '''
    def __init__(self,log=True):
        self.__records={}
        self.log=log
    def get_records(self):
        return self.__records
    def __deploy_nf(self,name,resource,node):
        vnfs=node.get_vnfs()
        for vnf in vnfs:
            if vnf.get_name()==name:
                remain_resource=vnf.get_remain_resource()
                d={}
                for key in resource:
                    data=remain_resource[key]-resource[key]
                    if data>=0:
                        d[key]=data
                    else:
                        if self.log==True:
                            print('log:  vnf in %s doesn\'t has enough resource %s(need %d,remain %d) for nf:%s'%(node.get_id(),key,resource[key],remain_resource[key],name))
                        return False
                vnf.set_remain_resource(d)
                return True
        if self.log==True:
            print('log:  ',node.get_id(),'doesn\'t has this type of vnf:',name)
        return False
    def deploy_nf(self,sfc,node,i):
        i=i-1
        name=sfc.get_nfs()[i]
        resource=sfc.get_nfs_detail()[name]
        if sfc.get_id() in self.__records:#防止双重部署
            if 'node' in self.__records[sfc.get_id()]:  
                if i+1 in self.__records[sfc.get_id()]['node']:
                    if self.log==True:
                        print('log:  you can\'t double deploy the nf(%d) in %s' %(i+1,sfc.get_id()))
                    return True
        if(self.__deploy_nf(name,resource,node)==True):
            if sfc.get_id() in self.__records:
                self.__records[sfc.get_id()]['node'][i+1]=node  
            else:
                self.__records[sfc.get_id()]={'node':{i+1:node},'edge':{}}
            return True
        else:
            return False
    def __add_vnf_types(self,name,resource,node,vnf_types):    #在节点中添加vnf，此函数只在__deploy_nf_scale_out中使用
        vnf_type=vnf_types.get_vnf_type(name)
        if vnf_type!=False:
            node.add_vnf(copy.deepcopy(vnf_type))
            if(node.scale_out_vnf(name,resource))==True:
                data={}
                for key in resource:
                    data[key]=0
                node.get_vnf(name).set_remain_resource(data)
                return True
            else:
                return False
        return False
    def __deploy_nf_scale_out(self,name,resource,node,vnf_types):  #以scale_out的方法部署资源
        vnfs=node.get_vnfs()
        for vnf in vnfs:
            if vnf.get_name()==name:
                remain_resource=vnf.get_remain_resource()
                scale_resource={}
                d={}
                for key in resource:
                    data=remain_resource[key]-resource[key]
                    if data>=0:
                        d[key]=data
                    else:
                        d[key]=0
                        scale_resource[key]=-data
                if scale_resource!={}:
                    if node.scale_out_vnf(name,scale_resource)==True:   #先伸缩扩大资源再设置剩余资源
                        vnf.set_remain_resource(d)
                        return True
                    else:
                        return False
                vnf.set_remain_resource(d)
                return True
        if self.__add_vnf_types(name,resource,node,vnf_types)==True: #如果vnf不存在，则添加节点再部署
            return True
        else:
            return False
        if self.log==True:
            print('log:  ',node.get_id(),'doesn\'t has this type of vnf:',name)
        return False
    def deploy_nf_scale_out(self,sfc,node,i,vnf_types):         #以scale_out的方法部署sfc的第i个vnf
        i=i-1
        name=sfc.get_nfs()[i]
        resource=sfc.get_nfs_detail()[name]
        if sfc.get_id() in self.get_records():#防止双重部署
            if 'node' in self.__records[sfc.get_id()]:  
                if i+1 in self.__records[sfc.get_id()]['node']:
                    if self.log==True:
                        print('log:  you can\'t double deploy the nf(%d) in %s' %(i+1,sfc.get_id()))
                    return True
        if(self.__deploy_nf_scale_out(name,resource,node,vnf_types)==True):
            if sfc.get_id() in self.get_records():
                self.get_records()[sfc.get_id()]['node'][i+1]=node  
            else:
                self.get_records()[sfc.get_id()]={'node':{i+1:node},'edge':{}}
            return True
        else :
            return False
    def __remove_nf(self,name,resource,node):
        vnfs=node.get_vnfs()
        for vnf in vnfs:
            if vnf.get_name()==name:
                for key in resource:
                    vnf.get_remain_resource()[key]+=resource[key]
                return True
        if self.log==True:
            print('log:  ',node.get_id(),'doesn\'t has this type of vnf:',name)
        return False
    def remove_nf(self,sfc,i):
        i=i-1
        node=self.__records[sfc.get_id()]['node'][i+1]
        name=sfc.get_nfs()[i]
        resource=sfc.get_nfs_detail()[name]
        if self.__remove_nf(name,resource,node)==True:
            return self.__records[sfc.get_id()]['node'].pop(i+1)
            
    def __deploy_link(self,network,node1,node2,att):
        if(node1==node2):
            return True
        data1=network.G[node1][node2]
        data={}
        for key in att:
            if key=='bandwidth':
                data['remain_bandwidth']=data1['remain_bandwidth']-att[key]
                if(data['remain_bandwidth']<0):
                    if self.log==True:
                        print('log:  link %s-%s doesn\'t has enough bandwidth' %(node1.get_id(),node2.get_id()))
                    return False
            else:
                data[key]=data1[key]-att[key]
                if(data[key]<0):
                    if self.log==True:
                        print('log:  link %s-%s doesn\'t has enough %d' %(node1.get_id(),node2.get_id(),key))
                    return False    
        return data
    def __record_edge(self,sfc_id,j,nodes):
        if sfc_id in self.__records:
            self.__records[sfc_id]['edge'][j]=nodes
        else:
            self.__records[sfc_id]={'node':{j:nodes},'edge':{}}
    def deploy_link(self,sfc,j,network,nodes):
        lens=len(nodes)
        datas=[]
        if(j not in self.__records[sfc.get_id()]['edge']):
            if j==1:#判断输入节点是否正确以及nf是否部署
                if nodes[0].get_id()==sfc.get_in_node() and self.__records[sfc.get_id()]['node'][j]==nodes[lens-1]:
                    for i in range(lens-1):
                        data=self.__deploy_link(network,nodes[i],nodes[i+1],{'bandwidth':sfc.get_bandwidths()[j-1]})
                        if data==False:
                            return False
                        else:
                            datas.append(data)
#                     for i in range(lens-1):
#                         network.set_edge_atts(nodes[i],nodes[i+1],datas[i])
                else:
                    if self.log==True:
                        print('log:  you must deploy the nodes at both ends of the link or endpoint error')
                    return False
            elif j==sfc.get_length()-1:#判断输出节点是否正确以及nf是否部署
                if self.__records[sfc.get_id()]['node'][j-1]==nodes[0] and nodes[lens-1].get_id()==sfc.get_out_node():
                    for i in range(lens-1):
                        data=self.__deploy_link(network,nodes[i],nodes[i+1],{'bandwidth':sfc.get_bandwidths()[j-1]})
                        if data==False:
                            return False
                        else:
                            datas.append(data)
#                     for i in range(lens-1):
#                         network.set_edge_atts(nodes[i],nodes[i+1],datas[i])     
                else:
                    if self.log==True:
                        print('log:  you must deploy the nodes at both ends of the link or endpoint error')
                    return False
            else:#判断nf是否部署
                if self.__records[sfc.get_id()]['node'][j-1]==nodes[0] and self.__records[sfc.get_id()]['node'][j]==nodes[lens-1]:
                    for i in range(lens-1):
                        data=self.__deploy_link(network,nodes[i],nodes[i+1],{'bandwidth':sfc.get_bandwidths()[j-1]})
                        if data==False:
                            return False
                        else:
                            datas.append(data)
#                     for i in range(lens-1):
#                         network.set_edge_atts(nodes[i],nodes[i+1],datas[i])       
                else:
                    if self.log==True:
                        print('log:  you must deploy the nodes at both ends of the link or endpoint error') 
                    return False
            for i in range(lens-1):
                if datas[i]!=True:
                    network.set_edge_atts(nodes[i],nodes[i+1],datas[i])   
            self.__record_edge(sfc.get_id(),j,nodes)
            return True
        else:
            if self.log==True:
                print('log:  you can\'t double deploy the virtual link(%d) in %s' %(j,sfc.get_id()))
            return False
    def __remove_link(self,network,node1,node2,att):
        if node1==node2:  #部署在同一个节点的虚拟路链路不占用资源
            return True
        for key in att:
            if key =='bandwidth':
                network.G[node1][node2]['remain_bandwidth']=network.G[node1][node2]['remain_bandwidth']+att[key]
            else:
                network.G[node1][node2][key]=network.G[node1][node2][key]+att[key]
        return True
    def remove_link(self,sfc,j,network): 
        edges=self.__records[sfc.get_id()]['edge'].pop(j)
        for i in range(len(edges)-1):
            self.__remove_link(network,edges[i],edges[i+1],{'bandwidth':sfc.get_bandwidths()[j-1]})
        return edges
    def remove_sfc(self,sfc,network):
        id1=sfc.get_id()
        record={'edge':{},'node':{}}
        keys=set(self.__records[id1]['edge'])
        for key in keys:
            record['edge'][key]=self.remove_link(sfc,key,network)
        del self.__records[id1]['edge']
        keys=set(self.__records[id1]['node'])
        for key in keys:
            record['node'][key]=self.remove_nf(sfc,key)
        del self.__records[id1]['node']
        other=self.__records.pop(id1)
#         record.update(other)
        return record
    def show(self):
        print('*************    print sfc deployed    **************')
        str1=''
        for sfc in self.__records:
            str1='%-8s:' %(str(sfc))
            for key in self.__records[sfc]:  #node edge
                str1=str1+'\n%-8s %-6s' %(' ',key+':')
                for key2 in self.__records[sfc][key]:
                    if(key=='node'):
                        str1=str1+'%-s-%-s ' %(key2,self.__records[sfc][key][key2].get_id())
                    else:
                        str1=str1+'%-s-[' %(key2)
                        for j in range(len(self.__records[sfc][key][key2])):
                            str1=str1+'%s ' %(self.__records[sfc][key][key2][j].get_id())
                        str1=str1+'] '
            print(str1)

class dynamic_scheduler(scheduler):
    '''
    dynamic_scheduler类,动态调度器类，提供SFC在线调度记录功能,详情见network基础类设计文档
    属性值：
        __record             记录单前sfc虚拟nf和虚拟链路的部署情况
        __history_record     记录历史记录
        __node_occupy_records记录节点占用记录
        __edge_occupy_records记录边占用记录
    属性方法：
        get_record
        depoly_nf
        remove_nf
        deploy_link
        remove_link
    '''
    def __init__(self,log=True):
#         scheduler.__init__(self)
        super(dynamic_scheduler, self).__init__(log=log)
        self.__records=super(dynamic_scheduler, self).get_records()
        self.__history_records=[]
        self.__node_occupy_records=[]
        self.__edge_occupy_records=[]
        self.T=1              #部署顺序为先auto_scheduling()，周期自增和释放资源，然后执行当前周期部署，第一周期不执行auto_scheduling
        self.sfc_records={}
    def get_timestamp(self):
        return self.T
    def get_records(self):
        return self.__records
    def get_history_records(self):
        return self.__history_records
    def get_node_occupy_records(self):
        return self.__node_occupy_records
    def get_edge_occupy_records(self):
        return self.__edge_occupy_records
    def occupy_node(self,network,node1,name='',atts={},time=0,vnf_types=[]): #占用节点部分资源，如果name==''，表示直接从节点占用资源，否则直接从节点的vnf占用资源
        if time >0:
            if type(node1)!= type(node()):
                node1=network.get_node(node1)
            if name!='':  #占用节点上vnf实例资源
                if super()._scheduler__deploy_nf_scale_out(name,atts,node1,vnf_types)==True:
                    record={'id':node1.get_id(),'name':name,'atts':atts,'time':time,'remain_time':time}
                    self.__node_occupy_records.append(record)
                    return True
                else:
                    return False
            else:        #占用节点资源
                remain_resource={}
                if node1.atts['access']!=True:
                    for key in atts :
                        if key in node1.remain_resource:
                            if node1.remain_resource[key]>=atts[key]:
                                remain_resource[key]=node1.remain_resource[key]-atts[key]
                            else:
                                if self.log==True:
                                    print('log:  vnf need ',key,' resource',atts[key],', but node only has ',node1.remain_resource[key],'.')
                                return False
                        else:
                            if self.log==True:
                                print('log:  node %s doesn\' t has this kind of resource:%s' %(node1.get_id(),key))
                            return False
                    for key in remain_resource:
                        node1.remain_resource[key]= remain_resource[key]
                record={'id':node1.get_id(),'name':name,'atts':atts,'time':time,'remain_time':time}
                self.__node_occupy_records.append(record)
                return True
        else:
            return True
    def occupy_edge(self,network,edge,att,time):     #占用链路的部分资源，edge为链路数组
        if time >0:
            l=len(edge)
            for i in range(l):
                if type(edge[i]) !=type(node()):
                    edge[i]=network.get_node(edge[i])
            datas=[]
            for i in range(l-1):
                node1=edge[i]
                node2=edge[i+1]
                if(node1!=node2):
                    data1=network.G[node1][node2]
                    data={}
                    for key in att:
                        if key=='bandwidth':
                            data['remain_bandwidth']=data1['remain_bandwidth']-att[key]
                            if(data['remain_bandwidth']<0):
                                if self.log==True:
                                    print('log:  link %d-%d doesn\'t has enough resource' %(node1.get_id(),node2.get_id()))
                                return False
                        else:
                            data[key]=data1[key]-att[key]
                            if(data[key]<0):
                                if self.log==True:
                                    print('log:  link %d-%d doesn\'t has enough resource' %(node1.get_id(),node2.get_id()))
                                return False    
                    datas.append(data)
            for i in range(l-1):
                network.set_edge_atts(edge[i],edge[i+1],datas[i]) 
            e=[]
            for ed in edge:
                e.append(ed.get_id())
            record={'id':e,'atts':att,'time':time,'remain_time':time}
            self.__edge_occupy_records.append(record)
            return True 
    def show_occupy_records(self):
        str1='******** shows additional utilization of node resources *********\n'
        str1+='%-3s%-25s%-15s%-5s%-7s%-s\n' %('','id','vnf','time','remain','atts')
        i=1
        for record in self.__node_occupy_records:
            str1+='%-3s%-25s%-15s%-5s%-7s%-s\n'%(i,record['id'],record['name'],record['time'],record['remain_time'],record['atts'])
            i+=1
        str2='******** shows additional utilization of edge resources *********\n'
        str2+='%-3s%-40s%-5s%-7s%-s\n' %('','id','time','remain','atts')
        i=1
        for record in self.__edge_occupy_records:
            str2+='%-3s%-40s%-5s%-7s%-s\n'%(i,record['id'],record['time'],record['remain_time'],record['atts'])
            i+=1
        print(str1,str2)
    def show_history_records(self,index=0):
        if index >self.T-1:
            print('*********************没有当前周期历史记录*********************')
        elif index !=0:
            history_record=self.__history_records[index-1]
            print('*************    print sfc history in period 3    **************')
            str1=''
            for sfc in history_record:
                str1='%-8s:' %(str(sfc))
                for key in history_record[sfc]:  #node edge
                    str1=str1+'\n%-8s %-6s' %(' ',key+':')
                    for key2 in history_record[sfc][key]:
                        if(key=='node'):
                            str1=str1+'%-s-%-s ' %(key2,history_record[sfc][key][key2].get_id())
                        else:
                            str1=str1+'%-s-[' %(key2)
                            for j in range(len(history_record[sfc][key][key2])):
                                str1=str1+'%s ' %(history_record[sfc][key][key2][j].get_id())
                            str1=str1+'] '
                print(str1)
        else:
            for i in range(self.T-1):
                history_record=self.__history_records[i]
                print('*************    print sfc history in period %d    **************' %(i+1))
                str1=''
                for sfc in history_record:
                    str1='%-8s:' %(str(sfc))
                    for key in history_record[sfc]:  #node edge
                        str1=str1+'\n%-8s %-6s' %(' ',key+':')
                        for key2 in history_record[sfc][key]:
                            if(key=='node'):
                                str1=str1+'%-s-%-s ' %(key2,history_record[sfc][key][key2].get_id())
                            else:
                                str1=str1+'%-s-[' %(key2)
                                for j in range(len(history_record[sfc][key][key2])):
                                    str1=str1+'%s ' %(history_record[sfc][key][key2][j].get_id())
                                str1=str1+'] '
                    print(str1) 
    def add_sfc_record(self,sfc):
        if sfc.get_id() in self.__records:
            if len(self.__records[sfc.get_id()]['node']) ==sfc.get_length()-2 and\
                len(self.__records[sfc.get_id()]['edge']) ==sfc.get_length()-1:
                self.sfc_records[sfc.get_id()]=sfc
            else:
                print('log: ************* you can\'t add an sfc record that is not fully deployed**************' )
    def show_sfc_records(self):
        for sfc_id in self.sfc_records:
            for index in range(len(self.__history_records)):
                if sfc_id in self.__history_records[index]:
                    print('***************************   生成周期：%d****************' %(index+2-self.sfc_records[sfc_id].get_duration()))
            self.sfc_records[sfc_id].show()

    def custom_process(self,network,sfc,record):
        return True
    def custom_process_all(self,network,sfc,records):
        return True
    def auto_scheduling(self,network):
        result=True
        records={}
        l=len(self.__edge_occupy_records)
        for i in range(l-1,-1,-1):               #删除边资源占用记录
            record=self.__edge_occupy_records[i]
            record['remain_time']-=1
            if record['remain_time']<=0:
                edges=record['id']
                for i in range(len(edges)-1):
                    super()._scheduler__remove_link(network,network.get_node(edges[i]),network.get_node(edges[i+1]),record['atts'])
                self.__edge_occupy_records.remove(record)

        l=len(self.__node_occupy_records)        #删除节点资源占用记录
        for i in range(l-1,-1,-1):
            record=self.__node_occupy_records[i]
            record['remain_time']-=1
            if record['remain_time']<=0:
                if record['name']!='': #释放占用vnf资源
                    super()._scheduler__remove_nf(record['name'],record['atts'],network.get_node(record['id']))
                else:                 #资源直接占用在node上，释放占用节点资源
                    node=network.get_node(record['id'])
                    atts=record['atts']
                    for key in atts:
                        node.remain_resource[key]=node.remain_resource[key]+atts[key]  
                self.__node_occupy_records.remove(record)

        for sfc_id in list(self.__records.keys()):        #转换成列表处理能够中途删除字段的key
            temporary_sfc=copy.deepcopy(self.sfc_records[sfc_id]) #临时拷贝这条可能会发生改变的sfc
            if self.sfc_records[sfc_id].next_cycle()==True:    #表示该条sfc状态发生改变，静态sfc永远不会发生状态改变
                records[sfc_id]=self.remove_sfc(temporary_sfc,network) #原始sfc内部资源已经更新，释放这条复制版sfc状态
                if self.sfc_records[sfc_id].is_life_end()==False:   #生命周期未结束，执行自定义custom_process函数
                    result=self.custom_process(network,self.sfc_records[sfc_id],records[sfc_id])
        self.__history_records.append(records)
        result=self.custom_process_all(network,self.sfc_records,records)  #对于上面未运行custom_process函数，也可以在这运行一次性处理所有改变sfc函数
        self.T+=1 
        return result
    