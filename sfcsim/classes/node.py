import copy
from sfcsim.classes.vnf import *
class node():
    '''
************************************************************************************************
    node类,表示网络中的一个节点，包含接入节点和服务器节点两种类型，详情见network基础类设计文档
    属性值：
        id                   节点id，节点唯一标识
        atts                 节点资源属性，可以有cpu、memory、stroage资源和access属性，表示是否为接入节点
        vnfs                 节点内部记录的vnf_type实例数组，包含资源(att),增加vnf占用节点资源
        remian_resource      剩余资源，节点中的剩余资源
        节点属性atts=节点剩余资源remian_resource+vnf属性atts
    属性方法：
        太多了，我不想写，主要包含get、set、show和针对vnf_type的add、delete方法

************************************************************************************************
    '''
    def __init__(self,uuid='node1',atts={'cpu':0,'memory':0,'storage':0,'access':False}):
        self.id=uuid
        self.atts={}
        self.vnfs=[]
        self.atts=copy.deepcopy(atts)
        self.remain_resource=copy.deepcopy(self.atts)
        self.remain_resource.pop('access')
    def set_id(self,uuid):
        self.id=uuid
    def get_id(self):
        return self.id
    def set_atts(self,atts):
        if(self.is_idle()==True):
            if 'access' in atts:
                if atts['access']==True:
                    for key in self.atts:
                        if key !='access':
                            self.atts[key]=0
                            self.remain_resource[key]=0
                    self.atts['access']=True
                    return True
                else:
                    for key in atts:
                        if key !='access':
                            self.atts[key]=atts[key]
                            self.remain_resource[key]=atts[key]
                    self.atts['access']=False
                    return True                    
            else:
                if self.is_access()==True:
                    print('log: you can\'t set access node resource attribute')
                    return False
            for key in atts:
                self.atts[key]=atts[key]
                self.remain_resource[key]=atts[key]
                return True
        else:
            print('log: node doen\'t idle, can\'t change attribute')
            return False
    def get_atts(self):
        return self.atts
    def set_access_node(self):
        if self.is_access()==False:
            if self.is_idle()==True:
                for key in self.atts:
                    if key !='access':
                        self.atts[key]=0
                        self.remain_resource[key]=0
                self.atts['access']=True
                return True
            else:
                print('log: set access fail!!!Can\'t set this node as access node because IT is occupied by VNF')
                return False
        else:
            print('log: Can\'t set this node as access node because it alerady is access node')
            return False
    def search_vnf_type(self,name):
        i=0
        for vnf in self.vnfs:
            if vnf.get_name()== name:
                return i
            else: i+=1
        return -1
    def add_vnf(self,vnf): #判断加入的数据是否未vnf_type类型
        remain_resource={}
        if type(vnf_type()) == type(vnf) and self.atts['access']!=True:
            if self.search_vnf_type(vnf.get_name())==-1:
                atts=vnf.get_atts()
                for key in atts :
                    if key in self.remain_resource:
                        if self.remain_resource[key]>=atts[key]:
                            remain_resource[key]=self.remain_resource[key]-atts[key]
                        else:
                            # print('log: add %s to node %s fail, vnf need %s resource %.2f, but node noly has %.2f' %(vnf.get_name(),self.id,key,atts[key],self.remain_resource[key]))
                            return False
                    else:
                        # print('log:  node doesn\' t has this kind of resource:',key)
                        return False
                for key in remain_resource:
                    self.remain_resource[key]= remain_resource[key]
                self.vnfs.append(vnf)
                return True
            else:
                # print('log:  add vnf fail,node aleardy has one instance of this type vnf')
                return False
    def delete_vnf(self,name):
        index=self.search_vnf_type(name)
        if index!=-1:
            if self.vnfs[index].is_idle()==True:
                remain_resource={}
                atts=self.vnfs[index].get_atts()
                for key in atts:
                    self.remain_resource[key]=self.remain_resource[key]+atts[key]  
                return self.vnfs.pop(index)
            else:
                print('delete fail!!!Can\'t delete VNF because IT is occupied by NF')
        else:
            print('delete fail!!!',name,'don\'t exist')
    def scale_in_vnf(self,name):   #缩小释放节点中vnf剩余资源
        index=self.search_vnf_type(name)
        if index!=-1:              #节点中存在该种类型vnf
            vnf_remain_resource={}      
            remain_resource=self.vnfs[index].get_remain_resource()
            for key in remain_resource :   #scale_in节点中vnf需要将vnf的remian_resource释放并修改vnf的atts，同时将节点remain_resource相应增加
                self.remain_resource[key]=self.remain_resource[key]+remain_resource[key]
                self.vnfs[index].get_atts()[key]-=remain_resource[key]
                vnf_remain_resource[key]=0
            self.vnfs[index].set_remain_resource(vnf_remain_resource)
            return True
        else:
            # print('log:   add vnf fail, node aleardy has one instance of this type vnf')
            return False
    def scale_out_vnf(self,name,atts):   #增加节点中vnf资源
        index=self.search_vnf_type(name)
        if index!=-1:              #节点中存在该种类型vnf
            remain_resource={}      
            for key in atts :      #检测节点中有没有这么多剩余资源
                if key in self.remain_resource:
                    if self.remain_resource[key]>=atts[key]:
                        remain_resource[key]=self.remain_resource[key]-atts[key]
                    else:
                        # print('log:   scale out vnf %s in node %s fail, vnf need %s resource %.2f, but node noly has %.2f' %(self.vnfs[index].get_name(),self.id,key,atts[key],self.remain_resource[key]))
                        return False
                else:
                    # print('log:  node doesn\' t has this kind of resource:',key)
                    return False
            
            for key in atts :   #scale_out节点中vnf需要将vnf的remian_resource增加并修改vnf的atts
                self.remain_resource[key]=remain_resource[key]    #更新节点中剩余资源
                self.vnfs[index].get_atts()[key]+=atts[key]
                self.vnfs[index].get_remain_resource()[key]+=atts[key]
            return True
        else:
            # print('log:   add vnf fail, node aleardy has one instance of this type vnf')
            return False
    def get_vnfs(self):
        return self.vnfs
    def get_vnf(self,name):
        for vnf in self.vnfs:
            if vnf.get_name()==name:
                return vnf
        return False
    def get_remain_resource(self):
        return self.remain_resource
    def is_access(self):
        return self.atts['access']
    def is_idle(self):
        for key in self.atts:
            if key !='access':
                if abs(self.atts[key]-self.remain_resource[key])>0.00000001:
                    return False
        return True
    def show(self):
        print('*****     show node:',self.id,'information     *****')
        print('id:',self.id,'idle:',self.is_idle(),'atts:',self.atts,'remain_resource:',self.remain_resource)
        i=1
        for vnf in self.vnfs:
            print('node vnf',i,':')
            vnf.show()
            i+=1
####

class nodes():
    '''
*************************************************************************************
    
    nodes类,表示所有node的集合，全局只应该有一个nodes实例,详情见network基础类设计文档
    属性值：
        number               node数量
        nodes                node类的所有实例，表示网络中存储的所有node实例
        __access_number      接入node数量
        __access_nodes       接入node类的所有实例
        __server_number      服务node数量
        __server_nodes       服务node类的所有实例
    属性方法：
        太多了，我不想写，主要包含get、set、search、add、delete、show五类方法
        
*************************************************************************************
    '''
    def __init__(self,nodes=[]):
        self.nodes=nodes
        self.number=len(self.nodes)
        self.__server_nodes=[]
        self.__access_nodes=[]
        for node in nodes:
            if node.is_access()==True:
                self.__access_nodes.append(node)
            else:
                self.__server_nodes.append(node)
        self.__access_number=len(self.__access_nodes)
        self.__server_number=len(self.__server_nodes)
    def get_number(self):
        return self.number
    def get_node(self,uuid):
        index=self.search_node(uuid)
        if index==-1:
            return False
        else :
            return self.nodes[index]
    def get_nodes(self):
        return self.nodes
    def get_access_nodes(self):
        return self.__access_nodes 
    def get_server_nodes(self):
        return self.__server_nodes
    def search_node(self,uuid):
        for i in range(self.number):
            if(self.nodes[i].get_id()==uuid):
                return i
            i+=1
        return -1
    def get_node(self,uuid):
        index=self.search_node(uuid)
        if index!= -1:
            return self.nodes[index]
        else:
            return False
    def search_access_node(self,uuid):
        for i in range(self.__access_number):
            if(self.__access_nodes[i].get_id()==uuid):
                return i
            i+=1
        return -1
    def search_server_node(self,uuid):
        for i in range(self.__server_number):
            if(self.__server_nodes[i].get_id()==uuid):
                return i
            i+=1
        return -1
    def add_node(self,node):
        if True:
            if self.search_node(node.get_id())==-1:
                self.nodes.append(node)
                self.number+=1
                if node.is_access():
                    self.__access_nodes.append(node)
                    self.__access_number+=1
                else:
                    self.__server_nodes.append(node)
                    self.__server_number+=1
                return True
            else:
                print('**********      node has exist     **********')
                return False
        else:
            print('log: attribute error!!! The parameter passed in must be node type')
            return False
    def add_nodes(self,nodes):
        for node in nodes:
            self.add_node(node)
    def delete_node(self,uuid):
        index=self.search_node(uuid)
        if index ==-1:              #节点不存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else:
            if self.nodes[index].is_idle()==True: #节点空闲，则可以删除，否则不可删除
                node=self.nodes.pop(index)
                self.number-=1
                if node.is_access():
                    self.__access_number-=1
                    return self.__access_nodes.pop(self.search_access_node(uuid))
                else:
                    self.__server_number-=1
                    return self.__server_nodes.pop(self.search_server_node(uuid))
            else:
                print('log: can delete',uuid,'node doesn\'t idle')
                return False
    def set_access_nodes(self,uuids):
        for uuid in uuids:
            index=self.search_node(uuid)
            if index ==-1:              #节点不存在
                print('**********     ',uuid,' node doesn\'t exist     **********')
                return False
            else: 
                if(self.nodes[index].set_access_node()==True):
                    node=self.__server_nodes.pop(self.search_server_node(uuid))
                    self.__server_number-=1 
                    self.__access_nodes.append(node)
                    self.__access_number+=1
    def set_atts(self,uuid,atts):
        index=self.search_node(uuid)
        if index ==-1:              #节点确实存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else:
            if('access' in atts):
                if self.nodes[index].is_access()==True and atts['access']==False:
                    if(self.nodes[index].set_atts(atts) ==True):
                        node=self.__access_nodes.pop(self.search_access_node(uuid))
                        self.__access_number-=1 
                        self.__server_nodes.append(node)
                        self.__server_number+=1
                elif self.nodes[index].is_access()==False and atts['access']==True:
                    if(self.nodes[index].set_atts(atts) ==True): 
                        node=self.__server_nodes.pop(self.search_server_node(uuid))
                        self.__server_number-=1 
                        self.__access_nodes.append(node)
                        self.__access_number+=1
                else:
                    self.nodes[index].set_atts(atts)
            else:
                self.nodes[index].set_atts(atts)
    def get_atts(self,uuid):
        index=self.search_node(uuid)
        if index ==-1:              #节点不存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else: 
            return self.nodes[index].get_atts()
    def get_remain_resource(self,uuid):
        index=self.search_node(uuid)
        if index ==-1:              #节点不存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else: 
            return self.nodes[index].get_remain_resource()
    def get_vnfs(self,uuid):
        index=self.search_node(uuid)
        if index ==-1:              #节点不存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else: 
            return self.nodes[index].get_vnfs()        
    def add_vnf(self,uuid,vnf):
        index=self.search_node(uuid)
        if index ==-1:              #节点不存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else: 
            self.nodes[index].add_vnf(vnf) 
                
    def delete_vnf(self,uuid,vnf_uuid):
        index=self.search_node(uuid)
        if index ==-1:              #节点不存在
            print('**********     ',uuid,' node doesn\'t exist     **********')
            return False
        else: 
            self.nodes[index].delete_vnf(vnf_uuid) 
    def show_access(self):
        print('*****    there are ',self.__access_number,'access nodes    *****')
        print('    %-6s    %-6s    %-62s    %-45s' %('number','id','att','remain_resource'))
        i=1
        for node in self.__access_nodes:
            print('    %-6d    %-6s    %-62s    %-45s' %(i,node.get_id(),node.get_atts(),node.get_remain_resource()))
            i+=1 
            
    def show_server(self):
        print('*****    there are ',self.__server_number,'server nodes    *****')
        print('    %-6s    %-6s    %-62s    %-45s' %('number','id','att','remain_resource'))
        i=1
        for node in self.__server_nodes:
            print('    %-6d    %-6s    %-62s    %-45s' %(i,node.get_id(),node.get_atts(),node.get_remain_resource()))
            i+=1 
            if node.is_idle()!=True:
                j=1
                print('                    vnf  number  type_name   ratio               att                              remain_resource')
                for vnf in node.get_vnfs():
                    print('                         %-6d  %-12s  %-3d  %-42s %-42s' %(j,vnf.get_name(),vnf.get_ratio(),vnf.get_atts(),vnf.get_remain_resource()))
                    j+=1           
    def show(self):
        print('*****    there are ',self.number,'nodes    *****')
        print('    %-6s    %-6s    %-62s    %-45s' %('number','id','att','remain_resource'))
        i=1
        for node in self.nodes:
            print('    %-6d    %-6s    %-62s    %-45s' %(i,node.get_id(),node.get_atts(),node.get_remain_resource()))
            i+=1 
            if node.is_idle()!=True:
                j=1
                print('                    vnf  number  type_name   ratio               att                              remain_resource')
                for vnf in node.get_vnfs():
                    print('                         %-6d  %-12s  %-3d  %-42s %-42s' %(j,vnf.get_name(),vnf.get_ratio(),vnf.get_atts(),vnf.get_remain_resource()))
                    j+=1