import copy

class vnf_type():
    '''
*************************************************************************************

    vnf_type类,表示一种类型的vnf，详情见network基础类设计文档
    属性值：
        name                 vnf类型
        atts                 vnf资源属性，只有节点中的vnf_type实例才能分配资源
        ratio                vnf流量伸缩属性，经过此vnf_type流量变化
        resorce_coefficient  资源系数，处理单位流量消耗资源
        remian_resource      剩余资源，只有节点中的vnf_type实例才有剩余资源
    属性方法：
        太多了，我不想写，注意包含get、set、show三类方法
        
************************************************************************************* 
    '''
    def __init__(self,name='vnf_type1',atts={'cpu':0,'memory':0,'storage':0},ratio=1,resource_coefficient={'cpu':1,'memory':1,'storage':1}):
        self.name=name
        self.atts=copy.deepcopy(atts)
        self.ratio=ratio
        self.resource_cofficient=copy.deepcopy(resource_coefficient)
        self.remain_resource=copy.deepcopy(atts)
        
    def set_name(self,name):
        self.name=name
    def get_name(self):
        return self.name
    def set_atts(self,atts_value={}):
        for key in atts_value:
            if key in self.atts:
                self.atts[key]=atts_value[key]
                self.remain_resource[key]=atts_value[key]
            else:
                print('warning!!!!atts has no attribute:',key)
    def get_atts(self):
        return self.atts
    def set_ratio(self,ratio):
        self.ratio=ratio
    def get_ratio(self):
        return self.ratio
    def set_coeff(self,coeff):
        for key in coeff:
            if key in self.resource_cofficient:
                self.resource_cofficient[key]=coeff[key]
            else:
                print('warning!!!! cofficient has no attribute:',key)
    def get_coeff(self):
        return self.resource_cofficient
    def set_remain_resource(self,resource):
        for key in resource:
            self.remain_resource[key]=resource[key]
    def get_remain_resource(self):
        return self.remain_resource
    def is_idle(self):
        for key in self.atts:
            if abs(self.atts[key]-self.remain_resource[key])>0.0000001:  #由于精度问题的判断两个小数是否相等的方法
                return False
        return True
    def show(self):
        print('name:',self.name,'idle:',self.is_idle(),' ratio:',self.ratio,' resource_coefficient:',self.resource_cofficient)
        print('atts:',self.atts,' remain_resource:',self.remain_resource)
        
class vnf_types():
    '''
************************************************************************************************

    vnf_types类,表示所有类型的vnf集合，全局只应该有一个vnf_types实例,详情见network基础类设计文档
    属性值：
        number               vnf_type数量
        vnf_types            存储vnf_type类的实例，表示网络中存储的所有vnf类型，不分配基础资源(att)
    属性方法：
        太多了，我不想写，主要包含get、set、search、add、delete、show五类方法
        
************************************************************************************************
    '''
    def __init__(self,number=0,vnf_types=[]):
        if(number>0 and vnf_types==[]):
            self.generate(number)
            self.number=number
        else:
            self.vnf_types=copy.deepcopy(vnf_types)
            self.number=len(vnf_types)
    def get_number(self):
        return self.number
    def generate(self,number):   #此方法一般不用，只用于快速神生成多个vnf类型
        self.number=number
        self.vnf_types=[]
        for i in range(1,self.number+1):
            self.vnf_types.append(vnf_type(name=('vnf_type'+str(i))))
    def search_vnf_type(self,name):
        for i in range(self.number):
            if self.vnf_types[i].get_name()== name:
                return i
        return -1
    def add_vnf_type(self,vnf_type1):
        if type(vnf_type()) == type(vnf_type1):
            if self.search_vnf_type(vnf_type1.get_name())==-1:
                self.vnf_types.append(vnf_type1)
                self.number+=1
            else:
                print('vnf type has already exists')
                return True
        else:
            print('type error')
            return False
    def delete_vnf_type(self,name):
        n=self.search_vnf_type(name)
        if n!=-1:
            self.number-=1
            return self.vnf_types.pop(n)
        else:
            print('this type of vnf doesn\'t exist')
            return False
    def delete_vnf_types(self,names):
        for name in names:
            self.delete_vnf_type(name)
    def get_vnf_type(self,name):
        n=self.search_vnf_type(name)
        if n!=-1:
            return self.vnf_types[n]
        else:
            print('this type of vnf doesn\'t exist')
            return False
    def get_vnf_types(self):
        return self.vnf_types
    def set_ratio(self,name,ratio):
        n=self.search_vnf_type(name)
        if n!=-1:
            self.vnf_types[n].set_ratio(ratio)
            return True
        else:
            print('this type of vnf doesn\'t exist')
            return False
    def get_ratio(self,name):
        n=self.search_vnf_type(name)
        if n!=-1:
            return self.vnf_types[n].get_ratio()
        else:
            print('this type of vnf doesn\'t exist')
            return False
    def set_coeff(self,name,coeff):
        n=self.search_vnf_type(name)
        if n!=-1:
            self.vnf_types[n].set_coeff(coeff)
            return True
        else:
            print('this type of vnf doesn\'t exist')
            return False
    def get_coeff(self,name):
        n=self.search_vnf_type(name)
        if n!=-1:
            return self.vnf_types[n].get_coeff()
        else:
            print('this type of vnf doesn\'t exist')
            return False
    def show(self):
        print('*****    there are ',self.number,'types of vnf    *****')
        print('    number    type_name     ratio         resouce_cofficient')
        i=0
        for vnf in self.vnf_types:
            print('    %-6d    %-12s    %-5s         %-s' %(i,vnf.get_name(),vnf.get_ratio(),vnf.get_coeff()))
            i+=1
