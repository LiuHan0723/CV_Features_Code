#!/usr/bin/env python
# coding: utf-8

# In[1]:


####################  ####################
#SK_data.py
#变量组：SK_data 大数据类所有/精通/熟练/良好/一般的技能数量
#输入数据集：
    # cv_basic_info_cleaned 基本信息表 
    # cv_skill_detail_cleaned 技能表
    # enum_skill 技能枚举值静态表
#输出数据集：
    # SK_data 
#作者：DXT
#版本：v0.1
####################  ####################


# In[2]:


#头文件
from header import *


# In[3]:


#变量计算逻辑（以pandas DataFrame传入计算该变量所需的数据集，返回含有id、各特征变量列的计算结果）
def cal_SK_data(df_cv_basic_info,df_cv_skill_detail,df_skill_enum):
    t1=pd.merge(df_cv_skill_detail,df_skill_enum,left_on='skill',right_on='skill',how='left')

    s1_1 = t1[t1['skill_type']=='大数据类'].groupby('id')['skill'].agg(SK_data_364=lambda x :x.count())
    s1_2 = t1[(t1['skill_type']=='大数据类')&(t1['level']=='精通')].groupby('id')['skill'].agg(SK_data_N_370=lambda x :x.count())
    s1_3 = t1[(t1['skill_type']=='大数据类')&(t1['level']=='熟练')].groupby('id')['skill'].agg(SK_data_1N_371=lambda x :x.count())
    s1_4 = t1[(t1['skill_type']=='大数据类')&(t1['level']=='良好')].groupby('id')['skill'].agg(SK_data_2N_372=lambda x :x.count())
    s1_5 = t1[(t1['skill_type']=='大数据类')&(t1['level']=='一般')].groupby('id')['skill'].agg(SK_data_3N_373=lambda x :x.count())
    
    s1=pd.concat([s1_1,s1_2,s1_3,s1_4,s1_5],axis=True).fillna(0)
    
    output=pd.merge(df_cv_basic_info[['id']],s1,left_on='id',right_on='id',how='left').fillna(0)
    return output


# In[4]:


if __name__=='__main__':
    
    #读入数据
    skill_enum=pd.read_excel(origin_path+"enum_skill.xlsx")
    cv_basic_info=pd.read_excel(input_path+"cv_basic_info_cleaned.xlsx")
    cv_skill_detail=pd.read_excel(input_path+"cv_skill_detail_cleaned.xlsx")
    
    result=cal_SK_data(cv_basic_info,cv_skill_detail,skill_enum)
    
    #输出计算结果
    writer=pd.ExcelWriter(output_path+"SK_data.xlsx",engine="openpyxl")
    result.to_excel(writer,index=False)
    writer.save()
    writer.close()
    
    #检查
    print(result.describe())

