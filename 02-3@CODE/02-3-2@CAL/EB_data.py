#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
import pandas as pd

from header import *
import datetime


# In[2]:


def cal_EB_data(df_cv_basic_info,df_education_info,df_intention_info,edu_level,edu_city,edu_rank,df_city_tier):
    
    degree_level_map={"博士":7,"硕士":6,"本科":5,"大专":4,"中技/中专":3,"高中":2,"初中及以下":1}

    df_cv_basic_info["degree"]=df_cv_basic_info["degree"].apply(lambda x:x.strip())
    df_cv_basic_info.set_index("id")
    df_cv_basic_info["EB_degree"]=df_cv_basic_info["degree"].map(degree_level_map)
    
    pd0=df_education_info.groupby("id").apply(lambda x: len(set(x["major"]))).to_frame()
    pd0.columns=["EB_major_N"]
    df_cv_basic_info=pd.merge(df_cv_basic_info,pd0,how="left",on="id")
    
    school_level={k:v for k,v in edu_level[["37_school_name","37_level"]].values}
    school_eval={"985":5,"211":4,"一本":3,"二本":2,"专科":1}
    school_rank={k:v for k,v in edu_rank[["38_school_name","38_rank"]].values}
    school_city={k:v for k,v in edu_city[["39_school_name","39_city"]].values}

    df_education_info["school_level"]=df_education_info["school"].map(school_level)
    df_education_info["EB_uni_rank1"]=df_education_info["school_level"].map(school_eval)
    df_education_info["EB_uni_rank2"]=df_education_info["school"].map(school_rank)




    tmp_bachelor_rank1=df_education_info[df_education_info["degree"]=="本科 "][["id","EB_uni_rank1"]]
    tmp_bachelor_rank1.columns=["id","EB_uni_rank1_01"]
    tmp_bachelor_rank2=df_education_info[df_education_info["degree"]=="本科"][["id","EB_uni_rank2"]]
    tmp_bachelor_rank2.columns=["id","EB_uni_rank2_02"]
    tmp_master_rank1=df_education_info[df_education_info["degree"]=="硕士"][["id","EB_uni_rank1"]]
    tmp_master_rank1.columns=["id","EB_mas_rank1_03"]
    tmp_master_rank2=df_education_info[df_education_info["degree"]=="硕士"][["id","EB_uni_rank2"]]
    tmp_master_rank2.columns=["id","EB_mas_rank2_04"]
    tmp_doctor_rank1=df_education_info[df_education_info["degree"]=="博士"][["id","EB_uni_rank1"]]
    tmp_doctor_rank1.columns=["id","EB_doc_rank1_05"]
    tmp_doctor_rank2=df_education_info[df_education_info["degree"]=="博士"][["id","EB_uni_rank2"]]
    tmp_doctor_rank2.columns=["id","EB_doc_rank2_06"]
    
    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_bachelor_rank1,how="left",left_on="id",right_on="id")
    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_bachelor_rank2,how="left",left_on="id",right_on="id")


    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_master_rank1,how="left",left_on="id",right_on="id")
    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_master_rank2,how="left",left_on="id",right_on="id")

    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_doctor_rank1,how="left",left_on="id",right_on="id")
    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_doctor_rank2,how="left",left_on="id",right_on="id")

    for col in range(len(df_cv_basic_info)):
        if pd.isna(df_cv_basic_info.loc[col,"EB_uni_rank2_02"] ):
            if df_cv_basic_info.loc[col,"degree"]=="本科":
                df_cv_basic_info.loc[col, "EB_uni_rank2_02"]=1000
            else:
                df_cv_basic_info.loc[col, "EB_uni_rank2_02"] = 2000

        if pd.isna(df_cv_basic_info.loc[col,"EB_mas_rank2_04"]):
            if df_cv_basic_info.loc[col,"degree"]=="硕士":
                df_cv_basic_info.loc[col, "EB_mas_rank2_04"]=1000
            else:
                df_cv_basic_info.loc[col, "EB_mas_rank2_04"] = 2000

        if pd.isna(df_cv_basic_info.loc[col, "EB_doc_rank2_06"] ):
            if df_cv_basic_info.loc[col, "degree"] == "博士":
                df_cv_basic_info.loc[col, "EB_doc_rank2_06"] = 1000
            else:
                df_cv_basic_info.loc[col, "EB_doc_rank2_06"] = 2000

    for col in range(len(df_education_info)):
        if df_education_info.loc[col,"end_time"]=="至今":
            year=str(int(df_education_info.loc[col,"begin_time"].split("-")[0])+4)
            month=df_education_info.loc[col,"begin_time"].split("-")[1]
            df_education_info.loc[col, "end_time"]="{}-{}".format(year,month)

    df_education_info["end_time"]=pd.to_datetime(df_education_info["end_time"])
    df_education_info["begin_time"]=pd.to_datetime(df_education_info["begin_time"])
    
    pd1=df_education_info.groupby("id").apply(lambda x:round(sum(i.days for i in x["end_time"]-x["begin_time"])/365,1)).to_frame()
    pd1.columns=["EB_edutime"]
    df_cv_basic_info=pd.merge(df_cv_basic_info,pd1,how="left",on="id")
    
    df_cv_basic_info["degree_city"]=df_cv_basic_info["school"].map(school_city)
    df_cv_basic_info["EB_City_add_02"]=np.array([i for i in df_cv_basic_info["degree_city"]==df_cv_basic_info["school"]]).astype(int)
    
    tmp_df=df_intention_info.groupby("id").apply(lambda x:list(x["intention_city"])).to_frame()
    tmp_df.columns=["city_list"]
    
    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_df,how="left",left_on="id",right_on="id")

    df_cv_basic_info["EB_City_EC_01"]=np.nan
    
    for i in range(len(df_cv_basic_info)):
    
        df_cv_basic_info.loc[i,"EB_City_EC_01"]=1 if df_cv_basic_info.loc[i,"degree_city"] in df_cv_basic_info.loc[i,"city_list"] else 0
        
    city_tier={k:v for k,v in df_city_tier.values}
    city_eval={"一线城市":4,"新一线城市":3,"二线城市":2,"三线城市":1,"三线以下":0}
    
    df_cv_basic_info["city_tier"]=df_cv_basic_info["degree_city"].map(city_tier)
    df_cv_basic_info["EB_City_tier_03"]=df_cv_basic_info["city_tier"].map(city_eval)
    
    tmp_df=df_education_info.groupby("id")["is_oversea"].sum().to_frame()
    tmp_df.columns=["EB_abr_num_01"]
    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_df,how="left",right_on="id",left_on="id")
    df_cv_basic_info.rename(columns={"abroad":"EB_abr1_02"},inplace=True)
    
    tmp_df=df_education_info[df_education_info["degree"]=="本科"]

    tmp_df=tmp_df[["id","is_oversea"]]

    tmp_df.rename(columns={"is_oversea":"EB_abr2_03"},inplace=True)

    df_cv_basic_info=pd.merge(df_cv_basic_info,tmp_df,how="left",right_on="id",left_on="id")

    df_cv_basic_info.drop_duplicates(subset=["id", "degree"], keep="first", inplace=True, ignore_index=False)
    return df_cv_basic_info[["id","EB_degree","EB_major_N","EB_uni_rank1_01","EB_uni_rank2_02","EB_mas_rank1_03",
                             "EB_mas_rank2_04","EB_doc_rank1_05","EB_doc_rank2_06","EB_edutime","EB_City_EC_01",
                             "EB_City_add_02","EB_City_tier_03","EB_abr_num_01","EB_abr1_02","EB_abr2_03"]].fillna(0).set_index("id")

# In[5]:


if __name__=="__main__":
    df_cv_basic_info=pd.read_excel("../../02-2@DATA/cv_basic_info_cleaned_IT.xlsx")
    df_education_info=pd.read_excel("../../02-2@DATA/cv_education_experience_cleaned_IT.xlsx")
    df_intention_info=pd.read_excel("../../02-2@DATA/cv_job_attention_cleaned_IT.xlsx")
    
    
    edu_level=pd.read_excel("../../02-2@DATA/简历变量设计-20220721-LF.xlsx",sheet_name="37_edu_level")
    edu_city=pd.read_excel("../../02-2@DATA/简历变量设计-20220721-LF.xlsx",sheet_name="39_edu_city")
    edu_rank=pd.read_excel("../../02-2@DATA/简历变量设计-20220721-LF.xlsx",sheet_name="38_edu_rank")
    
    df_city_tier=pd.read_excel("../../02-2@DATA/简历变量设计-20220721-LF.xlsx",sheet_name="31_city_tier")
    
    result=cal_EB_data(df_cv_basic_info,df_education_info,df_intention_info,edu_level,edu_city,edu_rank,df_city_tier)
    
    writer=pd.ExcelWriter(output_path+"EB_data.xlsx",engine="openpyxl")
    result.to_excel(writer)
    
    writer.save()
    writer.close()
    
    print(result.describe())
    


# In[ ]:




