from sfcsim.classes.sfc import *
class mobile_sfc(sfc):
    '''
    mobile_sfc类,输入节点随时间移动的sfc，详情见network基础类设计文档
    属性值：
        id                   sfc的唯一标识
        atts                 sfc的属性，包含以下：
            in_node    输入节点
            in_nodes   所有会移动到的输入节点
            out_node   输出节点
            nfs        网络功能集合
            bandwidths 链路带宽集合
            delay      延时需求
            duration   持续时间
            profit     利润
            nfs_detail nfs的一些细节信息(内部自动生成)
            type       sfc类型，内部自动生成，默认为1
        vnf_types      全局的vnf_types实例，现有的vnf_types才会有sfc
    属性方法：
        太多了，我不想写，主要包含get、set、show三类方法
    '''
    def __init__(self,uuid,in_nodes,out_node,nfs=[],bandwidth=0,delay=0,duration=0,profit=0,vnf_types=[]):
        if type(duration)==type([]):  #判断duration长度和in_nodes长度是否相同
            if len(in_nodes)!= len(duration):
                print('the length of duration must the same as the length of in_nodes')
                return False
        super(mobile_sfc, self).__init__(uuid=uuid,in_node=in_nodes[0],out_node=out_node,nfs=nfs,bandwidth=bandwidth,\
                                         delay=delay,duration=duration,profit=profit,vnf_types=vnf_types)
        self.atts['in_nodes']=in_nodes
        self.type=1
    def set_atts(self,atts):
        for key in atts:
            if key in self.atts or key=='bandwidth':
                if key =='nfs':
                    self.atts[key]=atts[key]
                    if vnf_types!=[]:
                        self.atts['bandwidths']=super()._sfc__calculate_link_bw(self.atts['bandwidths'][0])
                        self.atts['nfs_detail']=super()._sfc__calculate_resource(self.atts['nfs'])
                elif key =='nfs_detail':
                    print('error!!!you can\'t set nfs_detail, it is calaulated automatically')
                elif key =='in_nodes': 
                    self.atts[key]=atts[key]
                    self.atts['in_node']=atts[key][0]
                elif key =='nfs_detail':
                    print('error!!!you can\'t set nfs_detail, it is calaulated automatically')    
                elif key=='bandwidth':
                    if vnf_types!=[]:
                        self.atts['bandwidths']=super()._sfc__calculate_link_bw(atts[key])
                        self.atts['nfs_detail']=super()._sfc__calculate_resource(self.atts['nfs'])
                    else:
                        self.atts['bandwidths']=[bandwidth]
                else:
                    self.atts[key]=atts[key]
            else:
                print('warning!!! no such key:',key)
    def next_cycle(self):         #用于动态部署调度器中自动更新一些信息
        self.atts['service_time']+=1
        service_time=self.atts['service_time'] #service_time增加1
        if type(self.atts['duration'])==type([]):  #非周期变化对应判断单前位置方案
            index=-1
            while(service_time>=0):
                index=index+1
                if(index==len(self.atts['in_nodes'])-1): #到达最后一个周期
                    if self.atts['duration'][index]==0:  #最后一个周期为静态sfc
                        return False  
                    else:
                        service_time=service_time-self.atts['duration'][index]
                elif (index>len(self.atts['in_nodes'])-1): #超过最后一个周期
                    return True
                else:
                    service_time=service_time-self.atts['duration'][index]
        else:
            index=int(service_time/self.atts['duration']) #周期变化对应判断单前位置方案
            if (index>len(self.atts['in_nodes'])-1): #超过最后一个周期
                return True
        if self.atts['in_nodes'][index]==self.atts['in_node']: #没有更新输入节点，用户还未移动
            return False
        else:
            self.atts['in_node']=self.atts['in_nodes'][index] #已经更新输入节点，用户已移动
            return True
        
    def is_life_end(self): #在nest_cycle运行之后判断是否达到生命周期
        if type(self.atts['duration']) !=type([]): #duration设置为固定值
            if self.atts['service_time']>=self.atts['duration']*len(self.atts['in_nodes']):
                return True
            else:
                return False
        elif self.atts['duration'][len(self.atts['duration'])-1] ==0: #最后一周期为静态，永远不会结束
            return False
        else:
            service_time=self.atts['service_time']
            for data in self.atts['duration']:
                service_time=service_time-data
                if(service_time<0):
                    return False
        return True