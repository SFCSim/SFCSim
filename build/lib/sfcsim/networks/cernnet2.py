from sfcsim.classes.network import *
from sfcsim.classes.sfc import *
from sfcsim.layout.cernnet2_layout import *
class cernnet2(network):
    '''
    研究组实验室的开放挑战，挑战目标：在底层网络上部署文件中的sfc，算法执行时间短且总部署流量大者取胜
    属性值(cernnet继承network类，能使用network所有方法)：底层网络，网络拓扑为cernnet结构，详情见http://www.cernet20.edu.cn/introduction.shtml
        nodes               节点资源分布符合U(10~30) 
        G                   链路延迟符合U(0.5,1.5) (ms)
        vnf_types           vnf_types类实例，所有类型vnf集合，一共八种
        sfcs                sfcs类实例，所需部署目标服务功能链 
                                                       mMTC  30条 延迟分布U(5,10) 流量需求(0.1~0.5G) 长度 3~5nf
                                                       uRLLC 10条 延迟分布U(2,4) 流量需求(1~2G) 长度 1~2nf   
                                                       eMBB  6条 延迟分布U(5,10) 流量需求(3~4G) 长度 3~5nf    
    下列属性方法能够打印出底层数据结构：
        cernnet.vnf_types.show()
        cernnet.sfc.show()
        cernnet.show()
        cernnet.draw()
    '''
    def __init__(self):
        self.node1=node(uuid='node1',atts={'cpu':10,'access':False})
        self.node2=node(uuid='node2',atts={'cpu':10,'access':False})
        self.node3=node(uuid='node3',atts={'cpu':10,'access':False})
        self.node4=node(uuid='node4',atts={'cpu':10,'access':False})
        self.node5=node(uuid='node5',atts={'cpu':10,'access':False})
        self.node6=node(uuid='node6',atts={'cpu':10,'access':False})
        self.node7=node(uuid='node7',atts={'cpu':10,'access':False})
        self.node8=node(uuid='node8',atts={'cpu':10,'access':False})
        self.node9=node(uuid='node9',atts={'cpu':10,'access':False})
        self.node10=node(uuid='node10',atts={'cpu':10,'access':False})
        self.node11=node(uuid='node11',atts={'cpu':10,'access':False})
        self.node12=node(uuid='node12',atts={'cpu':10,'access':False})
        self.node13=node(uuid='node13',atts={'cpu':10,'access':False})
        self.node14=node(uuid='node14',atts={'cpu':10,'access':False})
        self.node15=node(uuid='node15',atts={'cpu':10,'access':False})
        self.node16=node(uuid='node16',atts={'cpu':10,'access':False})
        self.node17=node(uuid='node17',atts={'cpu':10,'access':False})
        self.node18=node(uuid='node18',atts={'cpu':10,'access':False})
        self.node19=node(uuid='node19',atts={'cpu':10,'access':False})
        self.node20=node(uuid='node20',atts={'cpu':10,'access':False})
        self.node21=node(uuid='node21',atts={'cpu':10,'access':False})
        server_nodes=[self.node1,self.node2,self.node3,self.node4,self.node5,self.node6,self.node7,self.node8,self.node9,self.node10,\
                   self.node11,self.node12,self.node13,self.node14,self.node15,self.node16,self.node17,self.node18,self.node19,self.node20,self.node21]
        access_nodes=[]
        network.__init__(self,server_nodes+access_nodes)
        self.generate_edges()
        self.generate_nodes_atts()
        self.generate_edges_atts()
        self.vnf_types=vnf_types(vnf_types=[(vnf_type(name='type1',atts={'cpu':0},ratio=0.8,resource_coefficient={'cpu':1}))\
                        ,vnf_type(name='type2',atts={'cpu':0},ratio=0.8,resource_coefficient={'cpu':1})\
                        ,vnf_type(name='type3',atts={'cpu':0},ratio=1.2,resource_coefficient={'cpu':1.8})\
                        ,vnf_type(name='type4',atts={'cpu':0},ratio=1.5,resource_coefficient={'cpu':1.5})\
                        ,vnf_type(name='type5',atts={'cpu':0},ratio=1,resource_coefficient={'cpu':1.4})\
                        ,vnf_type(name='type6',atts={'cpu':0},ratio=1,resource_coefficient={'cpu':1.2})\
                        ,vnf_type(name='type7',atts={'cpu':0},ratio=0.8,resource_coefficient={'cpu':1.2})\
                        ,vnf_type(name='type8',atts={'cpu':0},ratio=1,resource_coefficient={'cpu':2})])
        self.sfcs=sfcs([
        #uRTTC
        sfc('sfc31','node16','node20',['type1'],1.7,2,0,0,self.vnf_types),\
        sfc('sfc32','node5','node9',['type4'],1.4,2,0,0,self.vnf_types),\
        sfc('sfc33','node8','node19',['type5'],1.7,4,0,0,self.vnf_types),\
        sfc('sfc34','node16','node15',['type8', 'type6'],1.1,4,0,0,self.vnf_types),\
        sfc('sfc35','node12','node9',['type8'],1.0,3.5,0,0,self.vnf_types),\
        sfc('sfc36','node21','node13',['type2', 'type4'],1.3,4,0,0,self.vnf_types),\
        sfc('sfc37','node16','node8',['type7'],1.7,3,0,0,self.vnf_types),\
        sfc('sfc38','node3','node12',['type6'],1.2,3.1,0,0,self.vnf_types),\
        sfc('sfc39','node12','node21',['type4'],2.0,3,0,0,self.vnf_types),\
        sfc('sfc40','node3','node20',['type4', 'type8'],1.3,4,0,0,self.vnf_types),\
        #mMTC
        sfc('sfc1','node6','node11',['type1', 'type7', 'type4', 'type8', 'type2'],0.2,7,0,0,self.vnf_types),\
        sfc('sfc2','node21','node12',['type3', 'type6', 'type2', 'type8', 'type4'],0.2,10,0,0,self.vnf_types),\
        sfc('sfc3','node21','node17',['type6', 'type5', 'type4', 'type2'],0.4,9,0,0,self.vnf_types),\
        sfc('sfc4','node17','node13',['type1', 'type7', 'type3', 'type6', 'type2'],0.4,10,0,0,self.vnf_types),\
        sfc('sfc5','node11','node15',['type1', 'type8', 'type6'],0.5,10,0,0,self.vnf_types),\
        sfc('sfc6','node20','node3',['type7', 'type5', 'type4'],0.5,7,0,0,self.vnf_types),\
        sfc('sfc7','node2','node3',['type8', 'type6', 'type4', 'type1', 'type2'],0.2,7,0,0,self.vnf_types),\
        sfc('sfc8','node19','node3',['type4', 'type1', 'type2', 'type8', 'type7'],0.3,5,0,0,self.vnf_types),\
        sfc('sfc9','node19','node4',['type2', 'type5', 'type1', 'type6'],0.2,8,0,0,self.vnf_types),\
        sfc('sfc10','node15','node13',['type5', 'type7', 'type1', 'type2'],0.3,10,0,0,self.vnf_types),\
        sfc('sfc11','node9','node1',['type4', 'type6', 'type5', 'type1'],0.4,6,0,0,self.vnf_types),\
        sfc('sfc12','node19','node16',['type3', 'type2', 'type8', 'type7', 'type4'],0.2,5,0,0,self.vnf_types),\
        sfc('sfc13','node11','node10',['type7', 'type8', 'type5', 'type6'],0.2,10,0,0,self.vnf_types),\
        sfc('sfc14','node20','node6',['type1', 'type4', 'type3', 'type8'],0.3,6,0,0,self.vnf_types),\
        sfc('sfc15','node12','node20',['type7', 'type2', 'type3', 'type1'],0.4,9,0,0,self.vnf_types),\
        sfc('sfc16','node15','node8',['type8', 'type2', 'type1', 'type6', 'type5'],0.2,8,0,0,self.vnf_types),\
        sfc('sfc17','node1','node12',['type4', 'type5', 'type8', 'type7'],0.3,6,0,0,self.vnf_types),\
        sfc('sfc18','node19','node6',['type5', 'type7', 'type6', 'type1', 'type8'],0.1,10,0,0,self.vnf_types),\
        sfc('sfc19','node6','node4',['type1', 'type6', 'type5', 'type2'],0.4,6,0,0,self.vnf_types),\
        sfc('sfc20','node21','node6',['type7', 'type6', 'type2', 'type5', 'type8'],0.4,6,0,0,self.vnf_types),\
        sfc('sfc21','node6','node11',['type7', 'type1', 'type5'],0.1,10,0,0,self.vnf_types),\
        sfc('sfc22','node19','node12',['type6', 'type1', 'type8', 'type2', 'type4'],0.5,10,0,0,self.vnf_types),\
        sfc('sfc23','node21','node11',['type1', 'type6', 'type2', 'type4', 'type5'],0.1,10,0,0,self.vnf_types),\
        sfc('sfc24','node8','node17',['type3', 'type6', 'type1', 'type8'],0.3,9,0,0,self.vnf_types),\
        sfc('sfc25','node4','node18',['type4', 'type1', 'type7'],0.5,10,0,0,self.vnf_types),\
        sfc('sfc26','node14','node19',['type8', 'type6', 'type2', 'type3', 'type1'],0.2,7,0,0,self.vnf_types),\
        sfc('sfc27','node17','node12',['type3', 'type4', 'type8'],0.2,7,0,0,self.vnf_types),\
        sfc('sfc28','node15','node3',['type8', 'type3', 'type7', 'type5'],0.2,8,0,0,self.vnf_types),\
        sfc('sfc29','node21','node14',['type5', 'type3', 'type6', 'type8'],0.5,5,0,0,self.vnf_types),\
        sfc('sfc30','node4','node20',['type3', 'type4', 'type1', 'type5'],0.2,9,0,0,self.vnf_types),\
        #eMBB
        sfc('sfc41','node15','node14',['type8', 'type3', 'type6', 'type2', 'type5'],3.2,6,0,0,self.vnf_types),\
        sfc('sfc42','node10','node7',['type7', 'type2', 'type8', 'type3', 'type5'],3.0,7,0,0,self.vnf_types),\
        sfc('sfc43','node6','node8',['type5', 'type6', 'type1', 'type4'],3.8,8,0,0,self.vnf_types),\
        sfc('sfc44','node21','node3',['type8', 'type6', 'type5', 'type2'],3.1,8,0,0,self.vnf_types),\
        sfc('sfc45','node13','node15',['type2', 'type8', 'type4', 'type3', 'type7'],3.0,10,0,0,self.vnf_types),\
        sfc('sfc46','node17','node13',['type4', 'type5', 'type1', 'type3'],3.9,7,0,0,self.vnf_types),\
            ])
        self.figure=''
    def generate_edges(self):
        self.add_edges([[self.node1,self.node2,{'bandwidth':10}],[self.node2,self.node3,{'bandwidth':10}],\
                        [self.node3,self.node4,{'bandwidth':10}],[self.node3,self.node5,{'bandwidth':10}],\
                        [self.node5,self.node6,{'bandwidth':10}],[self.node5,self.node7,{'bandwidth':10}],\
                        [self.node5,self.node9,{'bandwidth':10}],[self.node5,self.node16,{'bandwidth':10}],\
                        [self.node6,self.node8,{'bandwidth':10}],[self.node7,self.node9,{'bandwidth':10}],\
                        [self.node8,self.node12,{'bandwidth':10}],[self.node9,self.node10,{'bandwidth':10}],\
                        [self.node10,self.node11,{'bandwidth':10}],[self.node12,self.node13,{'bandwidth':10}],\
                        [self.node12,self.node14,{'bandwidth':10}],[self.node13,self.node15,{'bandwidth':10}],\
                        [self.node14,self.node16,{'bandwidth':10}],[self.node15,self.node20,{'bandwidth':10}],\
                        [self.node16,self.node17,{'bandwidth':10}],[self.node16,self.node19,{'bandwidth':10}],\
                        [self.node16,self.node21,{'bandwidth':10}],[self.node17,self.node18,{'bandwidth':10}],[self.node20,self.node21,{'bandwidth':10}]])
    def generate_nodes_atts(self,atts=[30, 29, 28, 27, 27, 27, 26, 22, 22, 20, 19, 17, 16, 16, 14, 14, 13, 13, 12, 11, 10]):
        nodes=[5,16,21,3,12,13,10,1,2,4,6,7,8,9,11,14,15,17,18,19,20]
        if len(atts)==len(nodes):
            i=0
            for node in nodes:
                self.set_atts('node'+str(node),{'cpu':atts[i]})
                i+=1
    def generate_edges_atts(self,atts=[0.77, 0.59, 1.47, 0.95, 0.59, 0.69, 1.56, 1.1, 0.52, 1.03, 0.95, 1.08, 0.83, 1.21, 1.33, 0.92, 0.75, 1.34, 1.22, 1.29, 0.56, 0.64, 1.3]):
        i=0
        for edge in self.G.edges:
            self.set_edge_atts(edge[0],edge[1],{'delay':atts[i]})
            i+=1
    def draw(self,figsize=[36,20],node_size=10000,node_fone_size=8,link_fone_size=9,node_shape='H',path=''):
        network.draw(self,figsize=figsize,pos=cernnet2_layout(self.G),node_size=node_size,node_fone_size=node_fone_size,link_fone_size=link_fone_size,node_shape=node_shape)
    def draw_dynamic(self,figsize=[36,20],path='',node_size=10000,node_fone_size=8,link_fone_size=9,node_shape='H'):
        network.draw_dynamic(self,figsize=figsize,pos=cernnet2_layout(self.G),node_size=node_size,node_fone_size=node_fone_size,link_fone_size=link_fone_size,node_shape=node_shape)
