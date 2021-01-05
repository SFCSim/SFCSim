class nsfnet_layout_generate():
    def __init__(self): #棱长 
        self.__number=28
        self.__access_pos=[(-1.2,0.4),(-1.6,0),(-1.4,-0.4),(-1,0),(-0.6,-0.2),(-0.2,-0.6),(0,0),(0.4,0.2),(1,0),(0.6,-0.8),\
                           (0.8,0.6),(1.4,0.4),(1.2,-0.4),(1.6,0)]
        self.__server_pos=[]
        for data in self.__access_pos:
            data1=(data[0],data[1]-0.2)
            self.__server_pos.append(data1)
        self.__pos=self.__server_pos+self.__access_pos
    def layout(self,G):
        i=0
        pos2={}
        if len(G.nodes)>self.__number:
            print('Currently, NSfNET layout only supports %d nodes,but current are %d nodes' %(self.__number,len(G.nodes)))
            return -1
        for node in G.nodes:
            pos2[node]=self.__pos[i]
            i=i+1
        return pos2
def nsfnet_layout(G):
    return nsfnet_layout_generate().layout(G)