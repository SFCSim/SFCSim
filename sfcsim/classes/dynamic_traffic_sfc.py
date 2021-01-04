from sfcsim.classes.sfc import *
class dynamic_traffic_sfc(sfc):
    '''
    mobile_sfc类,输入节点随时间移动的sfc，详情见network基础类设计文档
    属性值：
        id                   sfc的唯一标识
        atts                 sfc的属性，包含以下：
            in_node    输入节点
            out_node   输出节点
            nfs        网络功能集合
            bandwidth  流量变化集合
            bandwidths 链路带宽集合
            delay      延时需求
            duration   持续时间
            profit     利润
            nfs_detail nfs的一些细节信息(内部自动生成)
            type       sfc类型，内部自动生成，默认为2
        vnf_types      全局的vnf_types实例，现有的vnf_types才会有sfc
    属性方法：
        太多了，我不想写，主要包含get、set、show三类方法
    '''
    def __init__(self,uuid,in_node,out_node,nfs=[],bandwidth=0,delay=0,duration=0,profit=0,vnf_types=[]):
        if type(duration)==type([]):  #判断duration长度和in_nodes长度是否相同
            if len(bandwidth)!= len(duration):
                print('the length of duration must the same as the length of bandwidth')
                return False
        super(dynamic_traffic_sfc, self).__init__(uuid=uuid,in_node=in_node,out_node=out_node,nfs=nfs,bandwidth=bandwidth[0],\
                                         delay=delay,duration=duration,profit=profit,vnf_types=vnf_types)
        self.atts['bandwidth']=bandwidth
        self.type=2
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
                elif key=='bandwidth':
                    if vnf_types!=[]:
                        self.atts['bandwidths']=super()._sfc__calculate_link_bw(atts[key][0])
                        self.atts['bandwidth']=atts[key]
                        self.atts['nfs_detail']=super()._sfc__calculate_resource(self.atts['nfs'])
                    else:
                        self.atts['bandwidths']=[atts[key][0]]
                        self.atts['bandwidth']=atts[key]
                else:
                    self.atts[key]=atts[key]
            else:
                print('warning!!! no such key:',key)
    def next_cycle(self):         #用于动态部署调度器中自动更新一些信息
        self.atts['service_time']+=1   #service_time增加1
        service_time=self.atts['service_time']
        if type(self.atts['duration'])==type([]): #非周期变化对应判断单前位置方案
            index=-1
            while(service_time>=0):
                index=index+1
                if(index==len(self.atts['bandwidth'])-1): #到达最后一个周期
                    if self.atts['duration'][index]==0:  #最后一个周期为静态sfc
                        return False  
                    else:
                        service_time=service_time-self.atts['duration'][index]
                elif (index>len(self.atts['bandwidth'])-1): #超过最后一个周期
                    return True
                else:
                    service_time=service_time-self.atts['duration'][index]
        else:                                   #周期变化对应判断单前位置方案
            index=int(service_time/self.atts['duration'])
            if (index>len(self.atts['bandwidth'])-1): #超过最后一个周期
                return True
        if self.atts['bandwidth'][index]==self.atts['bandwidths'][0]: #没有更新带宽，流量没有改变
            return False
        else:                   #已经更新带宽，sfc需求流量发生变化
            self.atts['bandwidths']=super()._sfc__calculate_link_bw(self.atts['bandwidth'][index])
            self.atts['nfs_detail']=super()._sfc__calculate_resource(self.atts['nfs'])
            return True
        
    def is_life_end(self): #在nest_cycle运行之后判断是否达到生命周期
        if type(self.atts['duration']) !=type([]): #duration设置为固定值
            if self.atts['service_time']>=self.atts['duration']*len(self.atts['bandwidth']):
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