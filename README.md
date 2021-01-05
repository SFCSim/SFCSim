# SFCSim
A general network function virtualization resource allocation simulation platform in Python language.  

- Source : [https://github.com/SFCSim/SFCSim](https://note.youdao.com/)
- Code&emsp;: [https://pypi.org/project/sfcsim/](https://note.youdao.com/)
# Dir

```
\- sfcsim/                                          main packet  
\         __init__.py  
\         classes/   
\                 __init__.py  
\                 vnf.py  
\                 ...  
\                 scheduler.py    
\         algorithms/  
\                    __init_\.py  
\                   common.py  
\                   ...  
\                   shortset_path_scheduler.py    
\         layout/  
\                __init_\.py    
\                cellular_layout.py  
\                cernnet2_layout.py  
\                nsfnet_layout.py  
\         networks/  
\                  __init__.py  
\                  cernnet2.py  
\                  nsfnet.py  
\  examples/                                        example codes  
\           classes/  
\                   vnf_type.py  
\                   sfc.py   
\                   network.py  
\                   ...  
\                   scheduler.py  
\           algorithms/  
\                      SA_scheduler.py   
\                      TS_scheduler.py  
\                      PSO_scheduler.py  
\                      shortest_path_scheduler.py  
\  doc/                                             Documentation  
\      SFCSim base class design.pdf  
\      algorithms/   
\                 SA_scheduler.pdf   
\                 TS_scheduler.pdf  
\                 PSO_scheduler.pdf  
\                 shortest_path_scheduler.pdf 
```
# Install
Install the latest version of SFCSim:

```
$ pip install sfcsim
```

# Simple example

```
## For more examples, see the examplez folder ##
>>> from sfcsim import *
>>> cernnet=cernnet2()          #实例化
>>> scheduler=shortest_path_scheduler()
>>> scheduler.deploy_sfcs(cernnet,cernnet.vnf_types,cernnet.sfcs,sort=True)  
>>> scheduler.show()
>>> print(len(scheduler.get_records()))
>>> cernnet.draw_dynamic(path='D:/result.png')
```

# Bugs
Please send email to xuly@bupt.edu.cn
# License
Released under the Apache License (see LICENSE.txt):

