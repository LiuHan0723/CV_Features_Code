#!/usr/bin/env python
# coding: utf-8

# In[1]:


from header import *


# In[34]:


def cal_SK_classification(df_basic_info,df_skill_info,enum_skill):
    
    skill_level={"无提及":0,"一般":1,"良好":2,"熟练":3,"精通":4}
    
    df_language_info=enum_skill[enum_skill["skill_type"]=="语言类"]
    
    df_other_info=enum_skill[enum_skill["skill_type"]!="语言类"]
    
    other_columns=["".join(i.split()) for i in pd.get_dummies(df_other_info["skill"]).columns]
    print(other_columns)
    
    df_skill_info["skill"]=["".join(i.split()) for i in df_skill_info["skill"]]
    
    df_skill_info["level_eval"]=df_skill_info["level"].map(skill_level)
    
    for c in other_columns:
        df_skill_info[c]=np.nan
    
    for s in range(len(df_skill_info)):
        if df_skill_info.loc[s,"skill"] in other_columns:
            df_skill_info.loc[s,df_skill_info.loc[s,"skill"]]=df_skill_info.loc[s,"level_eval"]
    
    language_columns=["".join(i.split()) for i in pd.get_dummies(df_language_info["skill"]).columns]
    
    for c in language_columns:
        df_skill_info[c]=np.nan
        
    
    for l in range(len(df_skill_info)):
        if df_skill_info.loc[l,"skill"] in language_columns:
            df_skill_info.loc[l,df_skill_info.loc[l,"skill"]]=df_skill_info.loc[l,"level_eval"]
            
    for c in other_columns:
        df_skill_info.rename(columns={c:"SK_ski_01"+c})


    for c in language_columns:
        df_skill_info.rename(columns={c:"SK_lan_02"+c})
    
    return df_skill_info.fillna(0)
    

    


# In[35]:


df_basic_info=pd.read_excel("../../02-2@DATA/result_html.xlsx",sheet_name="基本信息表")
df_skill_info=pd.read_excel("../../02-2@DATA/result_html.xlsx",sheet_name="技能表")
enum_skill=pd.read_excel("../../02-2@DATA/enum_skill.xlsx")
cal_SK_classification(df_basic_info,df_skill_info,enum_skill)


# In[29]:





# In[ ]:




