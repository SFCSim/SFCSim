class cernnet2_layout_generate():
    def __init__(self): #棱长 
        self.__number=42
        self.__server_pos=[(1.2,1.4),(1.2,0.9),(1,0.6),(0.9,0),(0,0),(0.3,-0.3),(-0.2,-0.5),(0.4,-0.6),(-0.3,-1),(-0.8,-1),\
                (-1.4,-1),(0.8,-1.3),(1.2,-1.3),(0.4,-1.4),(0.9,-1.6),(0,-1.6),(-1.1,-1.7),(-1.4,-1.7),(-0.2,-2),(0.9,-2.5),(0,-2.8)]
        self.__access_pos=[]
        for data in self.__server_pos:
            data1=(data[0]-0.2,data[1]-0.2)
            self.__access_pos.append(data1)
        self.__pos=self.__server_pos+self.__access_pos
    def layout(self,G):
        i=0
        pos2={}
        if len(G.nodes)>self.__number:
            print('Currently, CERNNET layout only supports %d nodes,but current are %d nodes' %(self.__number,len(G.nodes)))
            return -1
        for node in G.nodes:
            pos2[node]=self.__pos[i]
            i=i+1
        return pos2
def cernnet2_layout(G):
    return cernnet2_layout_generate().layout(G)