#!/usr/bin/env python
# coding: utf-8

# In[1]:


from header import *


# In[145]:


def cal_WE_size_data(df_basic_info,df_work_experience):
    
    
    size_level_map={"少于50人":1,"50-150人":2,"150-500人":3,"500-1000人":4,"1000-5000人":5," 5000-10000人":6,"10000人以上":7}
    df_work_experience["company_size"]=df_work_experience["company_size"].apply(lambda x:x.strip() if not pd.isna(x) else x )
    df_work_experience["size_level"]=df_work_experience["company_size"].map(size_level_map)
    df_work_experience=df_work_experience.replace({"end_time":{"至今":"2022/7"}})
    df_work_experience["begin_time"]=pd.to_datetime(df_work_experience["begin_time"])
    df_work_experience["end_time"]=pd.to_datetime(df_work_experience["end_time"])
   
    #最近一次工作的公司规模
    tmp_df=df_work_experience.groupby("id").apply(lambda x:x["size_level"].to_list()[0]).to_frame()
    tmp_df.columns=["WE_size_01"]
    df_basic_info=pd.merge(df_basic_info,tmp_df,how="left",on="id")
    
    df_basic_info=df_basic_info.set_index("id")
    for x in df_work_experience.groupby("id"):
        tmp_1x=x[1]["size_level"][x[1]["end_time"]>pd.to_datetime("2021/7")]
        tmp_2x=x[1]["size_level"][x[1]["end_time"]>pd.to_datetime("2020/7")]
        tmp_3x=x[1]["size_level"][x[1]["end_time"]>pd.to_datetime("2019/7")]
        tmp_4x=x[1]["size_level"][x[1]["end_time"]>pd.to_datetime("2018/7")]
        tmp_5x=x[1]["size_level"][x[1]["end_time"]>pd.to_datetime("2017/7")]
        
        if len(tmp_1x[~tmp_1x.isna()])>0:
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y1_size_MAX_02"]=max(tmp_1x[~tmp_1x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y1_size_MIN_03"]=min(tmp_1x[~tmp_1x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y1_size_MOD_04"]=tmp_1x[~tmp_1x.isna()].mode()[0]
            
        if len(tmp_2x[~tmp_2x.isna()])>0:
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y2_size_MAX_05"]=max(tmp_2x[~tmp_2x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y2_size_MIN_06"]=min(tmp_2x[~tmp_2x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y2_size_MOD_07"]=tmp_2x[~tmp_2x.isna()].mode()[0]
            
        if len(tmp_3x[~tmp_3x.isna()])>0:
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y3_size_MAX_08"]=max(tmp_3x[~tmp_3x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y3_size_MIN_09"]=min(tmp_3x[~tmp_3x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y3_size_MOD_10"]=tmp_3x[~tmp_3x.isna()].mode()[0]
            
        if len(tmp_4x[~tmp_4x.isna()])>0:
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y4_size_MAX_11"]=max(tmp_4x[~tmp_4x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y4_size_MIN_12"]=min(tmp_4x[~tmp_4x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y4_size_MOD_13"]=tmp_4x[~tmp_4x.isna()].mode()[0]
            
        if len(tmp_5x[~tmp_5x.isna()])>0:
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y5_size_MAX_14"]=max(tmp_5x[~tmp_5x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y5_size_MIN_15"]=min(tmp_5x[~tmp_5x.isna()])
            df_basic_info.loc[x[1]["id"].unique()[0],"WE_Y5_size_MOD_16"]=tmp_5x[~tmp_5x.isna()].mode()[0]
    
    return df_basic_info.loc[:,"WE_size_01":].fillna(0)

        
    
    
    


# In[146]:


df_basic_info=pd.read_excel("../../02-2@DATA/cv_basic_info_cleaned_IT.xlsx")
df_work_experience=pd.read_excel("../../02-2@DATA/cv_work_experience_cleaned_IT.xlsx")

print(cal_WE_size_data(df_basic_info,df_work_experience))


# In[142]:


df=df.replace({"end_time":{"至今":"2022/7"}})
df["begin_time"]=pd.to_datetime(df["begin_time"])
df["end_time"]=pd.to_datetime(df["end_time"])
# print(max(df["company_size"]))

df["test"]=0
df.loc["IT-H00000001","test"]=[1,1,1,1]
df["test"]


# In[56]:


max(np.nan,"dqw")


# In[110]:


df1=pd.DataFrame({"a":[1,2,3],"v":[5,6,7]})


# In[111]:


df1=df1.set_index("a")


# In[117]:


df1.loc[1,"d"]=1


# In[129]:


pd.Series([1,1,2]).mode()[0]


# In[ ]:




