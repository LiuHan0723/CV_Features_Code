#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####################  ####################
#pdf_pre_skill_detail.py
#功能：来自pdf的技能表数据清洗
#作者：DXT
#版本：v0.1
####################  ####################


# In[1]:


#头文件
from header import *


# In[2]:


#读入数据
cv_skill_detail=pd.read_excel(input_path+"result_pdf.xlsx",sheet_name="技能表")


# In[3]:


#清洗逻辑
#TO DO......
cv_skill_detail_cleaned=cv_skill_detail


# In[5]:


#输出清洗后结果
writer=pd.ExcelWriter(output_path+"cv_skill_detail_cleaned.xlsx",engine="openpyxl")
cv_skill_detail_cleaned.to_excel(writer,index=False)
writer.save()
writer.close()

