#!/usr/bin/env python
# coding: utf-8

# In[1]:


from header import *


# In[25]:


def cal_WE_size_EI_data(df_basic_info,df_job_intention,df_work_experience):
    
    df_job_intention=df_job_intention.set_index("id")
    size_level_map={"少于50人":1,"50-150人":2,"150-500人":3,"500-1000人":4,"1000-5000人":5," 5000-10000人":6,"10000人以上":7}
    df_work_experience["company_size"]=df_work_experience["company_size"].apply(lambda x:x.strip() if not pd.isna(x) else x )
    df_work_experience["size_level"]=df_work_experience["company_size"].map(size_level_map)
    
    df_basic_info=df_basic_info.set_index("id")
    
    for col in range(len(df_work_experience.index.unique())):
        
        idx=df_work_experience.loc[col,"id"]
        intention_industries=df_job_intention.loc[idx,"industry1":].values
        first_intention_industries=pd.Series(df_job_intention.loc[idx,"industry1"]).values
        
        if not pd.isna(df_work_experience.loc[col,"company_industry"]):
            
            if df_work_experience.loc[col,"company_industry"] in intention_industries:
                df_work_experience.loc[col,"is_intention_industry"]=True

            else:
                df_work_experience.loc[col,"is_intention_industry"]=False
        
            if df_work_experience.loc[col,"company_industry"] in first_intention_industries:
                df_work_experience.loc[col,"is_first_intention"]=True

            else:
                df_work_experience.loc[col,"is_first_intention"]=False
                
        else:
            df_work_experience.loc[col,"is_intention_industry"]=False
            df_work_experience.loc[col,"is_first_intention"]=False
    
    for x in df_work_experience.groupby("id"):
        tmp_1x=x[1]["size_level"][x[1]["is_intention_industry"]]
        tmp_2x=x[1]["size_level"][x[1]["is_first_intention"]]
        
        if len(tmp_1x[~tmp_1x.isna()])>0:
            
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EI_MAX_01"]=max(tmp_1x[~tmp_1x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EI_MIN_02"]=min(tmp_1x[~tmp_1x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EI_MOD_03"]=tmp_1x[~tmp_1x.isna()].mode()[0]
            
            
        if len(tmp_2x[~tmp_2x.isna()])>0:
        
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EI1_MAX_04"]=max(tmp_2x[~tmp_2x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EI1_MIN_05"]=min(tmp_2x[~tmp_2x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EI1_MOD_06"]=tmp_2x[~tmp_2x.isna()].mode()[0]
            
    return df_basic_info.loc[:,"WE_size_EI_MAX_01":].fillna(0)
        
        


# In[28]:


if __name__=="__main__":
    df_basic_info=pd.read_excel("../../02-2@DATA/cv_basic_info_cleaned_IT.xlsx")
    df_work_experience=pd.read_excel("../../02-2@DATA/cv_work_experience_cleaned_IT.xlsx")
    df_job_intention=pd.read_excel("../../02-2@DATA/cv_job_attention_cleaned_IT.xlsx")

    result=cal_WE_size_EI_data(df_basic_info,df_job_intention,df_work_experience)
    
    writer=pd.ExcelWriter(output_path+"WE_size_EI.xlsx",engine="openpyxl")
    result.to_excel(writer)
    
    writer.save()
    writer.close()
    print(result.describe())


# In[4]:


df=df.set_index("id")


# In[14]:


if 3 in np.array([[2,2],[2,1]]):
    print("a")


# In[30]:


pd.Series(pd.Series([1,2,3]))[[True,False,False]]


# In[ ]:




