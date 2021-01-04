from sfcsim.classes.network import *
import numpy as np
class network_matrix():
    '''
*************************************************************************************

    network_matrix类,矩阵形式的网络存储结构，可以直接转换为network类（）
    属性值：
        node_list            节点id数组
        edges                链路连接情况矩阵
        edge_atts            链路属性矩阵
    属性方法：
        太多了，我不想写，注意包含get、set、show三类方法
        
************************************************************************************* 
    '''
    def __init__(self,node_list=[],edge=[],edge_atts={}):
        self.node_list=copy.deepcopy(node_list)
        self.edge=copy.deepcopy(edge)
        self.edge_atts=copy.deepcopy(edge_atts)
    def generate(self,network1):  #从network类转换成network_matrix类
        self.node_list=[]
        for node in network1.get_nodes():
            self.node_list.append(node.get_id())
        self.edge=np.zeros((len(self.node_list),len(self.node_list)),int)
        edge=list(network1.G.edges)[0]
        for key in network1.G[edge[0]][edge[1]]:
            if key != 'remain_bandwidth':
                self.edge_atts[key]=np.zeros((len(self.node_list),len(self.node_list)))
        for edge in network1.G.edges:
            index1=self.node_list.index(edge[0].get_id())
            index2=self.node_list.index(edge[1].get_id())
            self.edge[index1][index2]=1
            for key in network1.G[edge[0]][edge[1]]:
                if key != 'remain_bandwidth':
                    self.edge_atts[key][index1][index2]=self.edge_atts[key][index2][index1]=network1.G[edge[0]][edge[1]][key]

    def set_node_list(self,node_list):
        self.node_list=node_list
    def get_node_list(self):
        return self.node_list
    
    def set_edge(self,edge):
        self.edge=edge
    def get_edge(self):
        return self.edge
    
    def set_edge_att(self,att,value):
        self.edge_atts[att]=value
    def set_edge_atts(self,att):
        for key in att:
            self.set_edge_att(key,att[key])
    def get_edge_att(self):
        return self.edge_atts[att]
    
    def update(self,edge=[],edge_atts={},node_list=[]):
        if edge!=[]:
            self.edge=edge
        if edge_atts!={}:
            for att in edge_atts:
                self.edge_atts[att]=edge_atts[att]
        if node_list!=[]:
            self.node_list=node_list
    def show(self):
        print('****************** Displays network link connections**************')
        str1='        '
        for node_id in self.node_list:
            str1=str1+('%-9s' %(node_id))

        for i in range(len(self.edge)):
            str2=('%-8s' %(self.node_list[i]))
            for data in self.edge[i]:
                str2+=('%-9s' %(data))
            str1+='\n'+str2
        print(str1)
        for att in self.edge_atts:
            print('****************** %s matrix**************' %(att))
            str1='        '
            for node_id in self.node_list:
                str1=str1+('%-9s' %(node_id))
            for i in range(len(self.edge_atts[att])):
                str2=('%-8s' %(self.node_list[i]))
                for data in self.edge_atts[att][i]:
                    str2+=('%-9s' %(data))
                str1+='\n'+str2
            print(str1)
        print('******************    END   **************')
class network_matrixs():
    '''
*************************************************************************************

    network_matrixs类,包含多个按照规律变化的network_matrix类
    属性值：
        network_matrix       network_matrix数组
        duration             每个周期持续时间
        
************************************************************************************* 
    '''
    def __init__(self,network_matrixs =[], duration=1):
        self.network_matrixs=network_matrixs
        self.duration=duration
    def get_network_matrix(self,t):
        if type(self.duration)==list:  #非周期变化对应判断单前位置方案
            index=-1
            while(t>0):
                index=(index+1)%len(self.network_matrixs)
                t=t-self.duration[index]
        else:
            index=(int((t-1)/self.duration))%len(self.network_matrixs) #周期变化对应判断单前位置方案
        return self.network_matrixs[index]
    def show(self):
        t=1
        for i in range(len(self.network_matrixs)):
            print('**************  the network state at time t:%d  ****************' %(t))
            self.network_matrixs[i].show()
            t=t+self.duration[i] if type(self.duration)==list else t+self.duration
