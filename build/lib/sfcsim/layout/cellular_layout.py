import math
class cellular_layout_generate():
    def __init__(self,R=1): #棱长 
        self.__number=5
        self.__cycle_number={}
        self.__angle={}
        self.__start_angle={}
        self.__R=R
        self.__r={0:[0],1:[self.__R*math.pow(3,0.5)],2:[self.__R*3,self.__R*2*math.pow(3,0.5)]}
        for i in range(1,3):
            self.__cycle_number[i]=6*i
            self.__angle[i]=2*math.pi/self.__cycle_number[i]
            if(i%2==0):
                self.__start_angle[i]=0;#math.atan(0.5*(math.pow(3,0.5))/(i*3/2))
            else:
                self.__start_angle[i]=math.atan(0.5*(math.pow(3,0.5))/((i-1)/2*3+1.5))
    def get_node_number(self,number):
        return 1+3*(number)*(number-1)
    def __zoom(self,datas):
        data1=[]
        for data in datas:
            data1.append((self.__R*data[0],self.__R*data[1]))
        return data1
    def __calculate_angle(self,cycle): #产生第cycle圈的坐标
        if cycle==0:
            coors=[(0,0)]
        elif cycle==3:
            coors=[(4.5,0.5*pow(3,0.5)),(4.5,1.5*pow(3,0.5)),(3,2*pow(3,0.5)),(1.5,2.5*pow(3,0.5)),\
                  (0,3*pow(3,0.5)),(-1.5,2.5*pow(3,0.5)),(-3,2*pow(3,0.5)),(-4.5,1.5*pow(3,0.5)),(-4.5,0.5*pow(3,0.5)),\
                  (-4.5,-0.5*pow(3,0.5)),(-4.5,-1.5*pow(3,0.5)),(-3,-2*pow(3,0.5)),(-1.5,-2.5*pow(3,0.5)),(0,-3*pow(3,0.5)),\
                  (1.5,-2.5*pow(3,0.5)),(3,-2*pow(3,0.5)),(4.5,-1.5*pow(3,0.5)),(4.5,-0.5*pow(3,0.5))] 
            coors=self.__zoom(coors)
        elif cycle==4:
            coors=[(6,0),(6,pow(3,0.5)),(6,2*pow(3,0.5)), (4.5,2.5*pow(3,0.5)), (3,3*pow(3,0.5)), (1.5,3.5*pow(3,0.5)),(0,4*pow(3,0.5)),\
                   (-1.5,3.5*pow(3,0.5)),(-3,3*pow(3,0.5)),(-4.5,2.5*pow(3,0.5)),(-6,2*pow(3,0.5)), (-6,pow(3,0.5)),(-6,0),\
                   (-6,-pow(3,0.5)),(-6,-2*pow(3,0.5)),(-4.5,-2.5*pow(3,0.5)),(-3,-3*pow(3,0.5)),(-1.5,-3.5*pow(3,0.5)),(0,-4*pow(3,0.5)),\
                   (1.5,-3.5*pow(3,0.5)),(3,-3*pow(3,0.5)),(4.5,-2.5*pow(3,0.5)),(6,-2*pow(3,0.5)),(6,-pow(3,0.5))]
            coors=self.__zoom(coors)
        else:
            coors=[]
            lens=len(self.__r[cycle])
            j=0
            for i in range(self.__cycle_number[cycle]):
                r=self.__r[cycle][j]
                angle=self.__start_angle[cycle]+i*self.__angle[cycle]
                coor=(r*math.cos(angle),r*math.sin(angle))
                j=(j+1)%lens
                coors.append(coor)
        return coors
    def calculate_angles(self,number):
        if number>self.__number:
            print('Currently, the cellular network supports only 5 layers,Automatically changes the number of layers to 5')
            number=5
        angles={}
        for i in range(number):
            angles[i]=self.__calculate_angle(i)
        return angles
    def layout(self,G):
        if len(G.nodes)>self.get_node_number(5):
            print('Currently, the cellular network supports only 5 layers,Automatically changes the number of layers to 5')
            return -1
        coords=self.calculate_angles(5)
        pos=[]
        for key in coords:
            pos=pos+coords[key]
        pos2={}
        i=0
        for node in G.nodes:
            pos2[node]=pos[i]
            i=i+1
        return pos2

def cellular_layout(G):
    return cellular_layout_generate().layout(G)