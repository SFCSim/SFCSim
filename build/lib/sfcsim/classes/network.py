import copy
import networkx as nx
from sfcsim.classes.node import *
from sfcsim.classes.vnf import *
from sfcsim.classes.network_matrix import *
import matplotlib.pyplot as plt
class network(nodes):
    '''
************************************************************************************************

    network类,继承nodes类，全局只应该有一个nodes实例,详情见network基础类设计文档
    network类除了继承nodes类之外还包含一个networkx.Graph实例，两者分别用于存储节点和链路信息，同时很多networkx
    原生的方法都可以使用，但修改节点链路等基础属性算法应该使用network类给出的下列方法
    属性值：
        包含nodes原有属性值
            number               node数量
            nodes                node类的所有实例，表示网络中存储的所有node实例
            __access_number      接入node数量
            __access_nodes       接入node类的所有实例
            __server_number      服务node数量
            __server_nodes       服务node类的所有实例
         G                       networkx.Graph实例，主要用于存储链路属性，节点属性为nodes类实例的引用
    属性方法：
        太多了，我不想写，包含nodes类原有方法，有些方法已经重载
        注意，对于添加节点链路等基础修改属性相关的功能应该使用network类方法，不用networkx原有方法(因为设计到节点属性)

************************************************************************************************
    '''
    def __init__(self,nodes1=[],network_matrix1=[]):
        nodes.__init__(self,nodes1)
        self.G=nx.Graph()
        self.generate()
        self.figure=''
        if(network_matrix1!=[]):
            data=self.update_edge(network_matrix1)
            self.change_edge(data[0],data[1],data[2])  
    def generate(self):
        for node in self.nodes:  #如果nodes的节点不再G中，则加入节点
            if node not in self.G:
                self.G.add_node(node)
        n=[]
        for node in self.G.nodes:           #如果G中的节点不再nodes中，则删除G中节点，一切以nodes中为准
            if node not in self.nodes:
                n.append(node)
        self.G.remove_nodes_from(n)
    def set_network_matrix(network_matrix1):
        data=self.update_edge(network_matrix1)
        self.change_edge(data[0],data[1],data[2])  
    def change_edge(self,edge_delete,edge_add,edge_att_change):
        self.delete_edges(edge_delete)
        self.add_edges(edge_add)
        self.set_edges_atts(edge_att_change)
        edges=edge_delete
        for edge in edge_add:
            edges.append([edge[0],edge[1]])
        for edge in edge_att_change:
            edges.append([edge0],[edge1])
        return edges

    def update_edge(self,network_matrix):
        edge_add=[] #[(node1,node2,atts)]
        edge_delete=[] #[[node1,node2],...]
        edge_att_change=[]# [[node1,node2,atts],...]
        lens=len(network_matrix.node_list)
        edges=self.G.edges
        for i in range(lens):
            for j in range(i+1,lens):
                if(network_matrix.edge[i][j]==0):  #下一状态不存在此edge
                    node0=self.get_node(network_matrix.node_list[i])
                    node1=self.get_node(network_matrix.node_list[j])
                    if (node0,node1) in edges:  #此状态中存在此edge，需要删除
                        edge_delete.append([node0,node1])
                
                else:                          #下一状态存在此edge
                    node0=self.get_node(network_matrix.node_list[i])
                    node1=self.get_node(network_matrix.node_list[j])
                    if (node0,node1) not in edges:  #此状态中不存在此edge，需要添加
                        atts={}
                        for att in network_matrix.edge_atts:
                            atts[att]=network_matrix.edge_atts[att][i][j]
                        edge_add.append([node0,node1,atts])
        return [edge_delete,edge_add,edge_att_change]
    def add_node(self,node):
        nodes.add_node(self,node)
        self.generate()
    def add_nodes(self,node_list):
        nodes.add_nodes(self,node_list)
        self.generate()  
    def delete_node(self,node1):
        if type(node()) == type(node1):
            if(nodes.delete_node(self,node1.get_id())!=False):
                self.G.remove_node(node1)
        else:
            data=nodes.delete_node(self,node1)
            if(data!=False):
                self.G.remove_node(data)
    def delete_nodes(self,node_list):
        for node in node_list:
            self.delete_node(node)
    def add_edge(self,node1,node2,**link):
        if type(node()) != (type(node1)):
            node1=self.get_node(node1)
        if type(node()) != (type(node2)):
            node2=self.get_node(node2)
        if node1==False or node2==False:
            print('log: error!!!node1 or node2 not in node list, can\'t add edge to node doesn\'t exists')
        else:
            if 'bandwidth' in link:
                link['remain_bandwidth']=link['bandwidth']
            self.G.add_edge(node1,node2,**link)
    def add_edges_from(self,edges):#edges格式为[(node1,node2,atts)]
        i=0
        edges2=[]
        for edge in edges:
            if type(node()) != (type(edge[0])):
                edge[0]=self.get_node(edge[0])
            if type(node()) != (type(edge[1])):
                edge[1]=self.get_node(edge[1])
            if edge[0] ==False or edge[1] ==False:
                print('log: error!!!can\'t add edge between nodes doesn\'t exist')
            else:
                edges2.append(edge)
            if 'bandwidth' in edge[2]:
                edge[2]['remain_bandwidth']=edge[2]['bandwidth']
            i+=1
        self.G.add_edges_from(edges2)
    def add_edges(self,edges):#edges格式为[(node1,node2,atts)]
        self.add_edges_from(edges)
    def delete_edge(self,node1,node2):
        if type(node()) != (type(node1)):
            node1=self.get_node(node1)
        if type(node()) != (type(node2)):
            node2=self.get_node(node2)
        if node1==False or node2==False:
            print('log: error!!!node1 or node2 not in node list, can\'t delete edge to node doesn\'t exists')
            return False
        else:
            try:
                self.G.remove_edge(node1,node2)
            except:
                return False
            else:
                return True
    def delete_edges(self,edges):
        for edge in edges:
            self.delete_edge(edge[0],edge[1])
    def delete_edges_from(self,edges):
        for edge in edges:
            self.delete_edge(edge[0],edge[1])
    def set_edge_atts(self,node1,node2,atts):
        if type(node()) != (type(node1)):
            node1=self.get_node(node1)
        if type(node()) != (type(node2)):
            node2=self.get_node(node2)
        if node1==False or node2==False:
            print('log: error!!!node1 or node2 not in node list, can\'t add edge atts to node doesn\'t exists')
            return False
        else:
            if 'bandwidth' in atts:
                atts['remain_bandwidth']=atts['bandwidth']
            nx.set_edge_attributes(self.G,{(node1,node2):atts})
            return True
    def set_edges_atts(self,atts):
        atts2={}
        for key in atts:
            if type(node()) != (type(key[0])):
                a=self.get_node(key[0])
            else:
                a=key[0]
            if type(node()) != (type(key[1])):
                b=self.get_node(key[1])
            else:
                b=key[1]
            if a==False or b==False:
                print('log: error!!!node1 or node2 not in node list, can\'t add edge atts to node doesn\'t exists')
            else:
                atts2[(a,b)]=atts[key]
        nx.set_edge_attributes(self.G,atts2)
    def show_nodes(self):
        nodes.show(self)         
    def show_edges(self):
        i=1
        print('*****     there are',len(self.G.edges),'edge in network     *****')
        print('    number  node1       node2       atts')
        for edge in self.G.edges.data():
            print('    %-6d  %-10s  %-10s  %-s' %(i,edge[0].get_id(),edge[1].get_id(),edge[2]))  
            i+=1
    def show(self):
        print('**********************     print nodes and edges in network     *********************')
        self.show_nodes()
        self.show_edges()

    # def draw(self,pos=[],figsize=[36,20],node_size=10000,node_fone_size=8,link_fone_size=9,node_shape='H',path=''):     #画图
    #     plt.figure(figsize=figsize)
    #     if(path!=''):
    #         fig=plt.gcf()
    #     node_labels ={}# nx.get_node_attributes(G)
    #     edge_label ={}# nx.get_edge_attributes(G)
    #     node_colors=[]
    #     node_sizes=[]
    #     for node in self.G.nodes:
    #         strs='ID: '+ str(node.get_id())+'\n' 
    #         if(node.is_access()==False):
    #             str1=('%-6s ' %('att'))
    #             str2=('%-6s ' %('all'))
    #             vnf_strs=[]
    #             for vnf in node.get_vnfs():
    #                 vnf_strs.append('%-6s ' %(str(vnf.get_name())))
    #             for key in node.get_atts():
    #                 if key != 'access':
    #                     str1=str1+('%-8s' %(str(key)))
    #                     stra=('%.3g/%.3g' %(node.get_remain_resource()[key],node.get_atts()[key]))
    #                     str2=str2+('%-8s' %(stra))
    #                     i=0
    #                     for vnf in node.get_vnfs():
    #                         stra=('%.3g/%.3g' %(vnf.get_remain_resource()[key],+vnf.get_atts()[key]))
    #                         vnf_strs[i]=vnf_strs[i]+('%-8s' %(stra))
    #                         i+=1
    #             node_colors.append('yellow') 
    #             node_sizes.append(node_size)
    #             strs=strs+str1+'\n'+str2
    #             for vnf_str in vnf_strs:
    #                 strs=strs+'\n'+vnf_str
    #         else:
    #             node_colors.append('red')
    #             node_sizes.append(18000)
    #         node_labels[node] = strs.rstrip('\n') 

    #     for edge in self.G.edges:
    #         strs=' '   
    #         for key in self.G.edges[edge]:
    #             if key =='bandwidth':
    #                 stra=('%.3g/%.3g' %(self.G.edges[edge]['remain_bandwidth'],self.G.edges[edge][key]))
    #                 strs=strs+'BW'+':'+stra+'\n'
    #             elif key!='remain_bandwidth':
    #                 strs=strs+key+':'+str(self.G.edges[edge][key])+'\n'
    #         edge_label[edge] = strs.rstrip('\n') 
    #     nx.draw(self.G,pos=pos,node_size=node_sizes,node_color=node_colors,width=2,edge_color='black',node_shape=node_shape)
    #     nx.draw_networkx_labels(self.G, pos=pos, labels=node_labels,font_size=node_fone_size)
    #     nx.draw_networkx_edge_labels(self.G, pos=pos,edge_labels=edge_label,font_size=link_fone_size)            
    #     plt.show()
    #     plt.close()
    #     if(path!=''):
    #         fig.savefig(path)
    def draw(self,pos=[],figsize=[36,20],node_size=10000,node_fone_size=8,link_fone_size=9,node_shape='H',path=''):     #画图，根据资源占用比显示10级别色差

        node_labels ={}# nx.get_node_attributes(G)
        edge_label ={}# nx.get_edge_attributes(G)
        node_colors=[]
        edge_colors=[]
        node_sizes=[]
        color_list=[]
        color_list1=[(200,0,0),(255,0,0),(255,30,30),(255,60,60),(255,90,90),(255,120,120),(255,150,150),(255,180,180),(255,210,210),(255,240,240)]
        for data in color_list1:
            color_list.append((data[0]/255,data[1]/255,data[2]/255))
        for node in self.G.nodes:
            color=0
            strs='ID: '+ str(node.get_id())+'\n' 
            if(node.is_access()==False):
                str1=('%-6s ' %('att'))
                str2=('%-6s ' %('all'))
                vnf_strs=[]
                for vnf in node.get_vnfs():
                    vnf_strs.append('%-6s ' %(str(vnf.get_name())))
                for key in node.get_atts():
                    if key != 'access':
                        str1=str1+('%-8s' %(str(key)))
                        stra=('%.3g/%.3g' %(node.get_remain_resource()[key],node.get_atts()[key]))
                        color+=node.get_remain_resource()[key]/node.get_atts()[key]
                        str2=str2+('%-8s' %(stra))
                        i=0
                        for vnf in node.get_vnfs():
                            stra=('%.3g/%.3g' %(vnf.get_remain_resource()[key],+vnf.get_atts()[key]))
                            vnf_strs[i]=vnf_strs[i]+('%-8s' %(stra))
                            i+=1
                color=int(round(10*color/(len(node.get_atts())-1))-1)
                if(color<0):
                    color=0
                node_colors.append(color_list[color]) 
                node_sizes.append(node_size)
                strs=strs+str1+'\n'+str2
                for vnf_str in vnf_strs:
                    strs=strs+'\n'+vnf_str
            else:
                node_colors.append('red')
                node_sizes.append(18000)
            node_labels[node] = strs.rstrip('\n') 
        for edge in self.G.edges:
            strs=' '   
            color=0
            for key in self.G.edges[edge]:
                if key =='bandwidth':
                    stra=('%.3g/%.3g' %(self.G.edges[edge]['remain_bandwidth'],self.G.edges[edge][key]))
                    color=int(round(10*self.G.edges[edge]['remain_bandwidth']/self.G.edges[edge][key])-1)
                    if(color<0):
                        color=0
                    strs=strs+'BW'+':'+stra+'\n'
                elif key!='remain_bandwidth':
                    strs=strs+key+':'+str(self.G.edges[edge][key])+'\n'
            edge_label[edge] = strs.rstrip('\n') 
            edge_colors.append(color_list[color])
        plt.figure(figsize=figsize)
        plt.ioff()
        if(path!=''):
            fig=plt.gcf()
        nx.draw(self.G,pos=pos,node_size=node_sizes,node_color=node_colors,width=4,edge_color=edge_colors,node_shape=node_shape)
        nx.draw_networkx_labels(self.G, pos=pos, labels=node_labels,font_size=node_fone_size)
        nx.draw_networkx_edge_labels(self.G, pos=pos,edge_labels=edge_label,font_size=link_fone_size) 
        plt.show()
        plt.close()
        if(path!=''):
            fig.savefig(path)
    def draw_dynamic(self,pos=[],figsize=[36,20],node_size=10000,node_fone_size=8,link_fone_size=9,node_shape='H',path=''):     #画图，根据资源占用比显示10级别色差
        node_labels ={}# nx.get_node_attributes(G)
        edge_label ={}# nx.get_edge_attributes(G)
        node_colors=[]
        edge_colors=[]
        node_sizes=[]
        color_list=[]
        color_list1=[(200,0,0),(255,0,0),(255,30,30),(255,60,60),(255,90,90),(255,120,120),(255,150,150),(255,180,180),(255,210,210),(255,240,240)]
        for data in color_list1:
            color_list.append((data[0]/255,data[1]/255,data[2]/255))
        for node in self.G.nodes:
            color=0
            strs='ID: '+ str(node.get_id())+'\n' 
            if(node.is_access()==False):
                str1=('%-6s ' %('att'))
                str2=('%-6s ' %('all'))
                vnf_strs=[]
                for vnf in node.get_vnfs():
                    vnf_strs.append('%-6s ' %(str(vnf.get_name())))
                for key in node.get_atts():
                    if key != 'access':
                        str1=str1+('%-8s' %(str(key)))
                        stra=('%.3g/%.3g' %(node.get_remain_resource()[key],node.get_atts()[key]))
                        color+=node.get_remain_resource()[key]/node.get_atts()[key]
                        str2=str2+('%-8s' %(stra))
                        i=0
                        for vnf in node.get_vnfs():
                            stra=('%.3g/%.3g' %(vnf.get_remain_resource()[key],+vnf.get_atts()[key]))
                            vnf_strs[i]=vnf_strs[i]+('%-8s' %(stra))
                            i+=1
                color=int(round(10*color/(len(node.get_atts())-1))-1)
                if(color<0):
                    color=0
                node_colors.append(color_list[color]) 
                node_sizes.append(node_size)
                strs=strs+str1+'\n'+str2
                for vnf_str in vnf_strs:
                    strs=strs+'\n'+vnf_str
            else:
                node_colors.append('red')
                node_sizes.append(18000)
            node_labels[node] = strs.rstrip('\n') 
        for edge in self.G.edges:
            strs=' '   
            color=0
            for key in self.G.edges[edge]:
                if key =='bandwidth':
                    stra=('%.3g/%.3g' %(self.G.edges[edge]['remain_bandwidth'],self.G.edges[edge][key]))
                    color=int(round(10*self.G.edges[edge]['remain_bandwidth']/self.G.edges[edge][key])-1)
                    if(color<0):
                        color=0
                    strs=strs+'BW'+':'+stra+'\n'
                elif key!='remain_bandwidth':
                    strs=strs+key+':'+str(self.G.edges[edge][key])+'\n'
            edge_label[edge] = strs.rstrip('\n') 
            edge_colors.append(color_list[color])
        if self.figure=='':
            self.figure=plt.figure(figsize=figsize)
            plt.ion() #开启interactive mode 成功的关键函数
        plt.clf() #清空画布上的所有内容
        if(path!=''):
            fig=plt.gcf()
        nx.draw(self.G,pos=pos,node_size=node_sizes,node_color=node_colors,width=4,edge_color=edge_colors,node_shape=node_shape)
        nx.draw_networkx_labels(self.G, pos=pos, labels=node_labels,font_size=node_fone_size)
        nx.draw_networkx_edge_labels(self.G, pos=pos,edge_labels=edge_label,font_size=link_fone_size)
        plt.show()
        if(path!=''):
            fig.savefig(path)