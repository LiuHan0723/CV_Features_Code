#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####################  ####################
#pdf_pre_basic_info.py
#功能：来自pdf的基本信息表数据清洗
#作者：DXT
#版本：v0.1
####################  ####################


# In[5]:


#头文件
from header import *


# In[8]:


#读入数据
cv_basic_info=pd.read_excel(input_path+"result_pdf.xlsx",sheet_name="基本信息表")


# In[9]:


#清洗逻辑
#TO DO......
cv_basic_info_cleaned=cv_basic_info


# In[10]:


#输出清洗后结果
writer=pd.ExcelWriter(output_path+"cv_basic_info_cleaned.xlsx",engine="openpyxl")
cv_basic_info_cleaned.to_excel(writer,index=False)
writer.save()
writer.close()

