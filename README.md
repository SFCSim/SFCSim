# SFCSim
A general network function virtualization resource allocation simulation platform in Python language.  

- Source: [https://github.com/SFCSim/SFCSim](https://note.youdao.com/)
# dir
\- sfcsim/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;main packet  
\-&emsp;&emsp;&emsp;&emsp;\_\_init\_\_.py  
\-&emsp;&emsp;&emsp;&emsp;classes/   
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\_\_init\_\_.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;vnf.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\.\.\.  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;scheduler.py    
\-&emsp;&emsp;&emsp;&emsp;algorithms/  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\_\_init\_\_.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;common.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\.\.\.  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;shortset_path_scheduler.py    
\-&emsp;&emsp;&emsp;&emsp;layout/  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\_\_init\_\_.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;cellular_layout.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;cernnet2_layout.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;nsfnet_layout.py  
\-&emsp;&emsp;&emsp;&emsp;networks/  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;\_\_init\_\_.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;cernnet2.py  
\-&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;nsfnet.py

\- examples/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;example codes  
\- &emsp;&emsp;&emsp;&emsp;&emsp;vnf_type.py  
\- &emsp;&emsp;&emsp;&emsp;&emsp;vnf_types.py  
\- &emsp;&emsp;&emsp;&emsp;&emsp;node.py  
\- &emsp;&emsp;&emsp;&emsp;&emsp;nodes.py   
\- &emsp;&emsp;&emsp;&emsp;&emsp;sfc.py   
\- &emsp;&emsp;&emsp;&emsp;&emsp;sfcs.py    
\- &emsp;&emsp;&emsp;&emsp;&emsp;network.py  
\- &emsp;&emsp;&emsp;&emsp;&emsp;scheduler.py  
\- &emsp;&emsp;&emsp;&emsp;&emsp;...   
\- &emsp;&emsp;&emsp;&emsp;&emsp;SA_scheduler.py   
\- &emsp;&emsp;&emsp;&emsp;&emsp;TS_scheduler.py

\- doc/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Documentation  
\-&emsp;&emsp;&emsp;\_\_init\_\_.py  
\-&emsp;&emsp;&emsp;SFCSim base class design.pdf  
\-&emsp;&emsp;&emsp;algorithms/ 
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

