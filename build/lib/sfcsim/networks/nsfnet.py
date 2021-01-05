# nsfnet底层网络类开发
from sfcsim.classes.network import *
from sfcsim.layout.cernnet2_layout import *
class nsfnet(network):
    def __init__(self,access=False):
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
        server_nodes=[self.node1,self.node2,self.node3,self.node4,self.node5,self.node6,self.node7,self.node8,self.node9,self.node10,\
                   self.node11,self.node12,self.node13,self.node14]
        if(access ==True):
            self.access1=node(uuid='access1',atts={'access':True})
            self.access2=node(uuid='access2',atts={'access':True})
            self.access3=node(uuid='access3',atts={'access':True})
            self.access4=node(uuid='access4',atts={'access':True})
            self.access5=node(uuid='access5',atts={'access':True})
            self.access6=node(uuid='access6',atts={'access':True})
            self.access7=node(uuid='access7',atts={'access':True})
            self.access8=node(uuid='access8',atts={'access':True})
            self.access9=node(uuid='access9',atts={'access':True})
            self.access10=node(uuid='access10',atts={'access':True})
            self.access11=node(uuid='access11',atts={'access':True})
            self.access12=node(uuid='access12',atts={'access':True})
            self.access13=node(uuid='access13',atts={'access':True})
            self.access14=node(uuid='access14',atts={'access':True})
            access_nodes=[self.access1,self.access2,self.access3,self.access4,self.access5,self.access6,self.access7,self.access8,\
                      self.access9,self.access10,self.access11,self.access12,self.access13,self.access14]
        else:
            access_nodes=[]
        super(nsfnet,self).__init__(server_nodes+access_nodes)
        self.generate_edges(access)
        self.generate_nodes_atts()
        self.generate_edges_atts()
    def generate_edges(self,access=False):
        if(access==True):
            self.add_edges([[self.node1,self.access1,{'bandwidth':10000}],[self.node2,self.access2,{'bandwidth':10000}],[self.node3,self.access3,{'bandwidth':10000}],\
                       [self.node4,self.access4,{'bandwidth':10000}],[self.node5,self.access5,{'bandwidth':10000}],[self.node6,self.access6,{'bandwidth':10000}],\
                       [self.node7,self.access7,{'bandwidth':10000}],[self.node8,self.access8,{'bandwidth':10000}],[self.node9,self.access9,{'bandwidth':10000}],\
                       [self.node10,self.access10,{'bandwidth':10000}],[self.node11,self.access11,{'bandwidth':10000}],[self.node12,self.access12,{'bandwidth':10000}],\
                       [self.node13,self.access13,{'bandwidth':10000}],[self.node14,self.access14,{'bandwidth':10000}]])
            self.add_edges([[self.access1,self.access2,{'bandwidth':100}],[self.access1,self.access4,{'bandwidth':100}],[self.access1,self.access8,{'bandwidth':100}],\
                       [self.access2,self.access3,{'bandwidth':100}],[self.access2,self.access4,{'bandwidth':100}],\
                       [self.access3,self.access6,{'bandwidth':100}],[self.access4,self.access5,{'bandwidth':100}],[self.access4,self.access11,{'bandwidth':100}],\
                       [self.access5,self.access6,{'bandwidth':100}],[self.access5,self.access7,{'bandwidth':100}],\
                       [self.access6,self.access10,{'bandwidth':100}],[self.access6,self.access13,{'bandwidth':100}],\
                       [self.access7,self.access8,{'bandwidth':100}],[self.access8,self.access9,{'bandwidth':100}],\
                       [self.access9,self.access10,{'bandwidth':100}],[self.access9,self.access12,{'bandwidth':100}],[self.access9,self.access14,{'bandwidth':100}],\
                       [self.access11,self.access12,{'bandwidth':100}],[self.access11,self.access14,{'bandwidth':100}],[self.access12,self.access14,{'bandwidth':100}],
                       [self.access13,self.access14,{'bandwidth':100}]])
        else:
            self.add_edges([[self.node1,self.node2,{'bandwidth':10}],[self.node1,self.node4,{'bandwidth':10}],[self.node1,self.node8,{'bandwidth':10}],\
                       [self.node2,self.node3,{'bandwidth':10}],[self.node2,self.node4,{'bandwidth':10}],\
                       [self.node3,self.node6,{'bandwidth':10}],[self.node4,self.node5,{'bandwidth':10}],[self.node4,self.node11,{'bandwidth':10}],\
                       [self.node5,self.node6,{'bandwidth':10}],[self.node5,self.node7,{'bandwidth':10}],\
                       [self.node6,self.node10,{'bandwidth':10}],[self.node6,self.node13,{'bandwidth':10}],\
                       [self.node7,self.node8,{'bandwidth':10}],[self.node8,self.node9,{'bandwidth':10}],\
                       [self.node9,self.node10,{'bandwidth':10}],[self.node9,self.node12,{'bandwidth':10}],[self.node9,self.node14,{'bandwidth':10}],\
                       [self.node11,self.node12,{'bandwidth':10}],[self.node11,self.node14,{'bandwidth':10}],[self.node12,self.node14,{'bandwidth':10}],
                       [self.node13,self.node14,{'bandwidth':10}]])
    def draw(self,node_size=40000,node_fone_size=15,link_fone_size=25,node_shape='H'):
        network.draw(self,pos=nsfnet_layout(self.G),node_size=node_size,node_fone_size=node_fone_size,link_fone_size=link_fone_size,node_shape=node_shape)

    def generate_nodes_atts(self,atts=[27, 26, 22, 22, 20, 19, 17, 16, 16, 14, 14, 13, 13]): #生成节点cpu属性
        nodes=[5,3,12,13,10,1,2,4,6,7,8,9,11,14]
        if len(atts)==len(nodes):
            i=0
            for node in nodes:
                self.set_atts('node'+str(node),{'cpu':atts[i]})
                i+=1
    def generate_edges_atts(self,atts=[0.47, 0.37, 1.33, 0.37, 0.49, 1.0, 0.37, 1.56, 0.47, 0.52, 0.68, 1.16, 0.37, 0.52, 0.74, 0.47, 0.49, 0.52, 0.82, 0.37, 0.47]):
        i=0
        for edge in self.G.edges:
            if edge[0].is_access()==False and edge[1].is_access()==False:
                self.set_edge_atts(edge[0],edge[1],{'delay':atts[i]})
                i+=1
    def draw(self,figsize=[40,20],node_size=40000,node_fone_size=15,link_fone_size=25,node_shape='H',path=''):
        network.draw(self,figsize=figsize,pos=nsfnet_layout(self.G),node_size=node_size,node_fone_size=node_fone_size,link_fone_size=link_fone_size,node_shape=node_shape,path=path)
    def draw_dynamic(self,path='',node_size=40000,node_fone_size=15,link_fone_size=25,node_shape='H'):
        network.draw_dynamic(self,pos=nsfnet_layout(self.G),node_size=node_size,node_fone_size=node_fone_size,link_fone_size=link_fone_size,node_shape=node_shape)
 