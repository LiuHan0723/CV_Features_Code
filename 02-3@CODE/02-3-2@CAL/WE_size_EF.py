#!/usr/bin/env python
# coding: utf-8

# In[1]:


from header import *


# In[6]:


def cal_WE_size_EF_data(df_basic_info,df_work_experience,df_job_intention):
    
    df_job_intention=df_job_intention.set_index("id")
    size_level_map={"少于50人":1,"50-150人":2,"150-500人":3,"500-1000人":4,"1000-5000人":5," 5000-10000人":6,"10000人以上":7}
    df_work_experience["company_size"]=df_work_experience["company_size"].apply(lambda x:x.strip() if not pd.isna(x) else x )
    df_work_experience["size_level"]=df_work_experience["company_size"].map(size_level_map)
    
    df_basic_info=df_basic_info.set_index("id")
    
    for col in range(len(df_work_experience.index.unique())):
        idx=df_work_experience.loc[col,"id"]
        intention_jobs=pd.Series(df_job_intention.loc[idx,"job"]).values
        first_intention_job=intention_jobs[0]
        if not pd.isna(df_work_experience.loc[col,"company_job"]):
            
            if df_work_experience.loc[col,"company_job"] in intention_jobs:
                df_work_experience.loc[col,"is_intention_job"]=True

            else:
                df_work_experience.loc[col,"is_intention_job"]=False
        
            if df_work_experience.loc[col,"company_job"] == first_intention_job:
                df_work_experience.loc[col,"is_first_job"]=True

            else:
                df_work_experience.loc[col,"is_first_job"]=False
                
        else:
            df_work_experience.loc[col,"is_intention_job"]=False
            df_work_experience.loc[col,"is_first_job"]=False
    
    for x in df_work_experience.groupby("id"):
        tmp_1x=x[1]["size_level"][x[1]["is_intention_job"]]
        tmp_2x=x[1]["size_level"][x[1]["is_first_job"]]
        
        if len(tmp_1x[~tmp_1x.isna()])>0:
            
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EF_MAX_01"]=max(tmp_1x[~tmp_1x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EF_MIN_02"]=min(tmp_1x[~tmp_1x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EF_MOD_03"]=tmp_1x[~tmp_1x.isna()].mode()[0]
            
            
        if len(tmp_2x[~tmp_2x.isna()])>0:
        
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EF1_MAX_04"]=max(tmp_2x[~tmp_2x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EF1_MIN_05"]=min(tmp_2x[~tmp_2x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_size_EF1_MOD_06"]=tmp_2x[~tmp_2x.isna()].mode()[0]
            
    return df_basic_info.loc[:,"WE_size_EF_MAX_01":].fillna(0)
        


# In[8]:


if __name__=="__main__":
    df_basic_info=pd.read_excel("../../02-2@DATA/cv_basic_info_cleaned_IT.xlsx")
    df_work_experience=pd.read_excel("../../02-2@DATA/cv_work_experience_cleaned_IT.xlsx")
    df_job_intention=pd.read_excel("../../02-2@DATA/cv_job_attention_cleaned_IT.xlsx")

    result=cal_WE_size_EF_data(df_basic_info,df_work_experience,df_job_intention)
    
    writer=pd.ExcelWriter(output_path+"WE_size_EF.xlsx",engine="openpyxl")
    result.to_excel(writer)
    
    writer.save()
    writer.close()
    print(result.describe())


# In[ ]:




