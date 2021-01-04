import copy
from sfcsim.classes.vnf import *
class sfc():
    '''
    sfc类,表示一条服务功能链请求，详情见network基础类设计文档
    属性值：
        id                   sfc的唯一标识
        atts                 sfc的属性，包含以下：
            in_node    输入节点
            out_node   输出节点
            nfs        网络功能集合
            bandwidths 链路带宽集合
            delay      延时需求
            duration   持续时间
            profit     利润
            nfs_detail nfs的一些细节信息(内部自动生成)
            type       sfc类型，内部自动生成，默认为0，表示静态或动态sfc
        vnf_types      全局的vnf_types实例，现有的vnf_types才会有sfc
    属性方法：
        太多了，我不想写，主要包含get、set、show三类方法
    '''
    def __init__(self,uuid,in_node,out_node,nfs=[],bandwidth=0,delay=0,duration=0,profit=0,vnf_types=[]):
        self.id=uuid
        self.atts={}
        self.atts['in_node']=in_node
        self.atts['out_node']=out_node
        self.atts['nfs']=copy.deepcopy(nfs)
        self.atts['delay']=delay
        self.atts['duration']=duration
        self.atts['profit']=profit
        self.atts['service_time']=0
        self.type=0
        self.vnf_types=vnf_types
        if vnf_types!=[]:
            self.atts['bandwidths']=self.__calculate_link_bw(bandwidth)
            self.atts['nfs_detail']=self.__calculate_resource(nfs)
        else:
            self.atts['bandwidths']=[bandwidth]
            self.atts['nfs_detail']={}
    def __calculate_link_bw(self,bandwidth): #根据vnf_type的流量伸缩系数计算所有虚拟链路所需带宽
        bw=[]
        bw.append(bandwidth)
        b=bandwidth
        for nf in self.atts['nfs']:
            b=100000000*b*(self.vnf_types.get_ratio(nf))/100000000  #防止出现很多小数点
            bw.append(b)
        return bw
    def __calculate_resource(self,nfs):  #根据所有虚拟链路带宽和vnf_type的coeff资源系数计算所有vnf占用资源，目前只有只支持线性
        atts={}
        i=0
        for nf in nfs:
            att={}
            coeff=self.vnf_types.get_coeff(nf)
            if isinstance(coeff,dict):
                for key in coeff:
                    att[key]=100000000*coeff[key]*self.atts['bandwidths'][i]/100000000
            else:
                att['cpu']=100000000*self.atts['bandwidths'][i]*coeff/100000000
            i+=1
            atts[nf]=att
        return atts
    def set_id(self,uuid):
        self.id=uuid
    def get_id(self):
        return self.id
    def get_length(self):
        return len(self.atts['nfs'])+2      
    def set_atts(self,atts):
        for key in atts:
            if key in self.atts or key=='bandwidth':
                if key =='nfs':
                    self.atts[key]=atts[key]
                    if vnf_types!=[]:
                        self.atts['bandwidths']=self.__calculate_link_bw(self.atts['bandwidths'][0])
                        self.atts['nfs_detail']=self.__calculate_resource(self.atts['nfs'])
                elif key =='nfs_detail':
                    print('error!!!you can\'t set nfs_detail, it is calaulated automatically')
                elif key=='bandwidth':
                    if vnf_types!=[]:
                        self.atts['bandwidths']=self.__calculate_link_bw(atts[key])
                        self.atts['nfs_detail']=self.__calculate_resource(self.atts['nfs'])
                    else:
                        self.atts['bandwidths']=[bandwidth]
                else:
                    self.atts[key]=atts[key]
            else:
                print('warning!!! no such key:',key)
    def get_atts(self):
        return self.atts
    def set_vnf_types(self,vnf_types1):
        if(type(vnf_types()) == type(vnf_types1)):
            self.vnf_types=vnf_types1
            self.atts['bandwidths']=self.__calculate_link_bw(self.atts['bandwidths'][0])
            self.atts['nfs_detail']=self.__calculate_resource(self.atts['nfs'])
        else:
            print('error!!!The parameter type needs to be vnf_types')
    def get_vnf_types(self):
        return self.vnf_types
    def get_nfs(self):
        return self.atts['nfs']
    def get_nfs_detail(self):
        return self.atts['nfs_detail']
    def get_bandwidths(self):
        return self.atts['bandwidths']
    def get_in_node(self):
        return self.atts['in_node']
    def get_out_node(self):
        return self.atts['out_node']
    def get_duration(self):
        return self.atts['duration']
    def get_service_time(self):   #获取服务时间，调度器中会自动增加这个时间，直到到达duration，静态部署不考虑
        return self.atts['service_time']
    def next_cycle(self):         #静态部署不考虑此函数，用于动态部署调度器中自动更新这个时间
        self.atts['service_time']+=1
        return self.is_life_end()  #只有有生命周期的sfc才会发生状态改变
    def is_life_end(self): #在nest_cycle运行之后判断是否达到生命周期
        if self.atts['duration'] ==0: #静态sfc，永远不会结束
            return False
        else:
            if self.atts['service_time']>= self.atts['duration']:
                return True
            else:
                return False
        return True
    def get_profit(self):
        return self.atts['profit']
    def get_delay(self):
        return self.atts['delay']
    def get_type(self):
        return self.type
    def show(self):
        strs='      '
        print('ID:%s type:%d' %(self.id,self.type))
        for att in self.atts:
            if (att == 'nfs' or att == 'nfs_detail') == False:
                strs=strs+str(att)+':'+str(self.atts[att])+', '
        print(strs)
        if(self.vnf_types!=[]):
            print('      number  nfs                   detail')
            i=1
            for nf in self.atts['nfs']:
                print('      %-6d  %-10s           %-43s' %(i,nf,self.atts['nfs_detail'][nf]))
                i+=1
        else:
            print('      number  nfs')
            i=1
            for nf in self.atts['nfs']:
                print('      %-6d  %-10s' %(i,nf))
                i+=1
        
class sfcs():
    '''
    sfcs类,表示所有sfc的集合，全局只应该有一个sfcs实例,详情见network基础类设计文档
    属性值：
        number               vnf_type数量
        sfcs                 存储sfc类的实例，表示所有sfc类型
    属性方法：
        太多了，我不想写，主要包含get、set、search、add、delete、show五类方法
    '''
    def __init__(self,sfcs=[]):
        self.number=len(sfcs)
        self.sfcs=copy.deepcopy(sfcs)
    def get_number(self):
        return self.number
    def search_sfc(self,uuid):
        for i in range(self.number):
            if self.sfcs[i].get_id()==uuid:
                return i
        return -1
    def get_sfcs(self):
        return self.sfcs
    def add_sfc(self,sfc1):
        if self.search_sfc(sfc1.get_id())==-1:
            self.sfcs.append(sfc1)
            self.number+=1
            return True
        else:
            print('error!the SFC ID:',sfc1.get_id(),'already exists!')
            return False
    def delete_sfc(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            self.sfcs.pop(index)
            self.number-=1
            return True
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_sfc(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index]
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def pop_sfc(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            self.number-=1
            return self.sfcs.pop(index)
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_length(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_length()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False   
    def set_atts(self,uuid,atts):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].set_atts(atts)
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_atts(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_atts()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def set_vnf_types(self,uuid,vnf_types):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].set_vnf_types(vnf_types)
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_vnf_types(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_vnf_types()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_nfs(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_nfs()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_nfs_detail(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_nfs_detail()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_bandwidths(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_bandwidths()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_in_node(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_in_node()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_in_node(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_in_node()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_out_node(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_out_node()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_duration(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_duration()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_delay(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_delay()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_type(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_type()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def get_profit(self,uuid):
        index=self.search_sfc(uuid)
        if index!=-1:
            return self.sfcs[index].get_profit()
        else:
            print('error!!!the SFC with ID:',uuid,'don\'t exists')
            return False
    def show(self):
        print('*****    there are ',self.number,'sfcs    *****')
        print('%-6s %-8s %-7s %-8s %-5s %-8s %-6s %-32s %-s' %('number','id','in_node','out_node','delay','duration','profit','bandwidths', 'nfs'))
        i=1
        for sfc in self.sfcs:
            print('%-6d %-8s %-7s %-8s %-5d %-8d %-6d %-32s %-s' %(i,sfc.get_id(),sfc.get_in_node(),sfc.get_out_node(),\
                                                               sfc.get_delay(),sfc.get_duration(),sfc.get_profit(),\
                                                               sfc.get_bandwidths(),sfc.get_nfs()))
            i+=1

    def show_detail(self):
        print('*****    there are ',self.number,'sfcs    *****')
        print('%-6s %-8s %-7s %-8s %-5s %-8s %-6s %-32s %-s' %('number','id','in_node','out_node','delay','duration','profit','bandwidths', 'nfs'))
        i=1
        for sfc in self.sfcs:
            print('%-6d %-8s %-7s %-8s %-5d %-8d %-6d %-32s %-s' %(i,sfc.get_id(),sfc.get_in_node(),sfc.get_out_node(),\
                                                               sfc.get_delay(),sfc.get_duration(),sfc.get_profit(),\
                                                               sfc.get_bandwidths(),sfc.get_nfs()))
            i+=1
            if(sfc.vnf_types!=[]):
                print('              nfs                   detail')
                for nf in sfc.atts['nfs']:
                    print('              %-10s           %-43s' %(nf,sfc.atts['nfs_detail'][nf]))