import numpy as np
def show_solutions(solutions,sfc_id):
    print(sfc_id,'   ',len(solutions[sfc_id]))
    for solution in solutions[sfc_id]:
        print('        ',solution)
def find_all_path(graph,start,end,path=[]):  # 找到网络里一个节点到另一个节点的所有路径
    path = path +[start]
    if start == end:
        return [path]
    paths = [] #存储所有路径    
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_path(graph,node,end,path) 
            for newpath in newpaths:
                paths.append(newpath)
    return paths
def find_network_all_path(graph): #找到网络所有路径
    paths={}
    nodes=graph.nodes
    for node1 in nodes:
        paths[node1]={}
        for node2 in nodes:
            if node2 !=node1:
                paths[node1][node2]=find_all_path(graph,node1,node2)
    return paths
def is_condition_met(datas): #判断datas数组后边的数是否比前面大
    lens=len(datas)-1
    for j in range(lens):
        if(datas[j]>datas[j+1]):
            return False
    return True
def count_mode(nf_number,node_number): #给出单条路径上符合条件的部署方案
    sum=int((node_number**nf_number-1))
    deploy=[]
    for count in range(sum+1):
        datas=np.zeros((nf_number,), dtype=int)
        data=count
        i=0
        while(data>0):
            datas[nf_number-1-i]=(data%node_number)
            data=int(data/node_number)
            i=i+1
        if is_condition_met(datas)==True:
            deploy.append(list(datas))
    return deploy
def get_deploy_from(path,sfc,mode):
    lens=len(mode)
    solution={'node':{},'edge':{}}
    for i in range(lens):
        solution['node'][i+1]=path[mode[i]].get_id()  #记录nf部署方案
        edge=[]
        if i ==0:                                     #记录虚拟链路部署方案
            for j in range(mode[0]+1):
                edge.append(path[j].get_id())
        else:
            for j in range(mode[i-1],mode[i]+1):
                edge.append(path[j].get_id())
        if len(edge)==0:                 #表示部署在节点内部的方法
            edge=[path[mode[i-1]].get_id(),path[mode[i-1]].get_id()]
        elif len(edge)==1:
            edge.append(edge[0])
        solution['edge'][i+1]=edge
        
    edge=[]
    for j in range(mode[lens-1],len(path)):
        edge.append(path[j].get_id())
    if len(edge)==1:
        edge.append(sfc.get_out_node())
    solution['edge'][lens+1]=edge
    return solution
def find_sfc_solution(path,sfc): #找到一个网络里对于一条sfc的所有解决方案，以字符串record的格式存储
    nf_number=sfc.get_length()-2
    node_number=len(path)
    deploy_modes=count_mode(nf_number,node_number)
    solution=[]
    for mode in deploy_modes:
        solution.append(get_deploy_from(path,sfc,mode))
    return deploy_modes,solution
def get_path_delays(network,path):
    lens=len(path)-1
    delay=0
    for i in range(lens):
        delay=delay+network.G[path[i]][path[i+1]]['delay']
    return delay
def find_sfcs_solutions(network,sfcs,n=1):#找到网络里所有sfc的所有部署方案，以字典格式存储{'sfc1':[{},{},{}]}
    all_paths=find_network_all_path(network.G)
    all_solutions={}
    all_modes={}
    for sfc in sfcs.get_sfcs():
        all_solutions[sfc.get_id()]=[]
        solutions=[]
        modes=[]
        sfc_paths=all_paths[network.get_node(sfc.get_in_node())][network.get_node(sfc.get_out_node())]
        path_length=[]
        for path in sfc_paths:  #对路径进行筛选，支取延迟最小的n条
            path_length.append(get_path_delays(network,path))
        index=np.array(path_length).argsort()
        lens=n if len(sfc_paths)>n else len(sfc_paths)
        sfc_paths2=[]
        for i in range(lens):
            sfc_paths2.append(sfc_paths[index[i]])
        for path in sfc_paths2:
            if get_path_delays(network,path)<sfc.get_delay(): #满足条件的路径
                mode,solution=find_sfc_solution(path,sfc)
                modes.extend(mode)
                solutions.extend(solution) #获取sfc在这条路径下的所有部署方案
        all_modes[sfc.get_id()]=modes      
        all_solutions[sfc.get_id()]=solutions
    return all_modes,all_solutions
def records_node_to_str(records):        #将node类的部署记录转化为字符串形式的部署记录
    new_records={}
    for sfc_id in records:
        new_records[sfc_id]={'node':{},'edge':{}}
        for key in records[sfc_id]:
            if key =='node':
                for num in records[sfc_id][key]:
                    new_records[sfc_id][key][num]=records[sfc_id][key][num].get_id()
            elif key =='edge':
                for num in records[sfc_id][key]:
                    path=[]
                    for node in records[sfc_id][key][num]:
                        path.append(node.get_id())
                    new_records[sfc_id][key][num]=path
    return new_records
def records_str_to_num(records,all_sfc_deploy_records):  #将字符串类的部署记录转化为数字形式的部署记录
    new_records={}
    for sfc_id in all_sfc_deploy_records:
        if sfc_id in records :
            if (records[sfc_id] !=-1) :
                lens=len(all_sfc_deploy_records[sfc_id])
                for i in range(lens):
                    if(all_sfc_deploy_records[sfc_id][i] == records[sfc_id]):
                        new_records[sfc_id]=i
            else:
                new_records[sfc_id]=-1
        else:
            new_records[sfc_id]=-1
    return(new_records)