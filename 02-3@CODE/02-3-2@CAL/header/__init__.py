#!/usr/bin/env python
# coding: utf-8

# In[1]:


####################  ####################
#__init__.py
#功能：变量计算头文件
#作者：DXT
#版本：v0.1
####################  ####################


# In[2]:


#导包
import os
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import warnings
warnings.filterwarnings("ignore")


# In[3]:


#读入数据的路径
origin_path=os.path.dirname(os.path.dirname(os.getcwd()))+"\\02-1@INPUT\\"
input_path=os.path.dirname(os.path.dirname(os.getcwd()))+"\\02-2@DATA\\"
output_path=os.path.dirname(os.path.dirname(os.getcwd()))+"\\02-4@OUTPUT\\"

