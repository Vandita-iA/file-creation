import pandas as pd
import psycopg2 as pg

master_df = pd.read_excel('/home/vandita/Documents/BI voice/30 April/Masters/Ring_For_Business_Master_30_April.xlsx')

# try:
#     connection = pg.connect(
#         host="192.168.1.189",
#         port="5432",
#         database="dev_voice",
#         user="postgres",
#         password="Password123*"
#     )
#     print('Connection is On')
# except Exception as e:
#     print(e)

# query = "SELECT DISTINCT campaign_name FROM public.data_distribution_master"
# cursor = connection.cursor()
# cursor.execute(query)
# campaign_name_list = cursor.fetchall()

# campaign_name = input(f"Select campaign name: {campaign_name_list}") #Take single choice user input here
# query = "SELECT * FROM public.data_distribution_master where campaign_name = '%s'" % campaign_name 
# master_df= pd.DataFrame()
# try:
#     master_df = pd.read_sql_query(query, connection)
# except:
#     print('Error: Unable to fetch data from the database')
# finally:
#     connection.commit()
#     connection.close()
#     print('Connection closed')

print(master_df)

maxout = True # take user input here as a checkbox, keep it initially disabled
if maxout:
    master_df.loc[(master_df['last_updated_disposition'] == 'Lead For Qualification') & (master_df['maxout'].isna()), 'maxout'] = 'MAXOUT'

websites = master_df.loc[master_df['last_updated_disposition'] == 'Lead For Qualification', 'website'].tolist()
companies = master_df.loc[master_df['last_updated_disposition'] == 'Lead For Qualification', 'company'].tolist()

df = master_df.loc[
    (master_df['dd'].isnull()) &
    (master_df['ab_user'].isnull()) &
    (master_df['maxout'].isnull()) &
    (master_df['dnc'].isnull()) &
    (master_df['suppressed'].isnull())].copy()

df['project'] = df['campaign_name']

print(df)

last_updated_group1_values = input(f"Select required group1: {df['last_updated_group1'].unique()}") # Replace with actual multiplechoice user input
last_updated_group1_list = last_updated_group1_values.split(',')
if 'None' in last_updated_group1_list:    
    last_updated_group1_list.remove('None')
    df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list) | df['last_updated_group1'].isnull()]
elif 'nan' in last_updated_group1_list:    
    df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list) | df['last_updated_group1'].isnull()]
else:
    df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list)]

print(df)
last_updated_date_values = input(f"Select NOT required date: {df['last_updated_date'].unique()}") # Replace with actual multiplechoice user input
last_updated_date_list = last_updated_date_values.split(',')
df = df.loc[~df['last_updated_date'].isin(last_updated_date_list) | df['last_updated_date'].isnull()]

print(df)
last_updated_group_values = input(f"Select required group: {df['last_updated_group'].unique()}") # Replace with actual multiplechoice user input
last_updated_group_list = last_updated_group_values.split(',')
if 'None' in last_updated_group_list:
    last_updated_group_list.remove('None')
    df = df.loc[df['last_updated_group'].isin(last_updated_group_list) | df['last_updated_group'].isnull()]
elif 'nan' in last_updated_group_list:
    df = df.loc[df['last_updated_group'].isin(last_updated_group_list) | df['last_updated_group'].isnull()]
else:
    df = df.loc[df['last_updated_group'].isin(last_updated_group_list)]

print(df)

df['last_updated_disposition'] = df['last_updated_disposition'].astype(str).str.replace("Not Available, Try Again", "Not Available - Try Again")
print(df['last_updated_disposition'])
last_updated_disposition =df['last_updated_disposition'].unique()

last_updated_disposition_values = input(f"Select required disposition: {last_updated_disposition}") # Replace with actual multiplechoice user input
last_updated_disposition_list = last_updated_disposition_values.split(',')
if 'None' in last_updated_disposition_list:
    last_updated_disposition_list.remove('None')
    df = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list) | df['last_updated_disposition'].isnull()]
elif 'nan' in last_updated_disposition_list:
    print(last_updated_disposition_list)
    print(last_updated_disposition_list)
    df1 = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list)]
    df2 = df.loc[df['last_updated_disposition'].isnull()]
    df = final_df = pd.concat([df1, df2], axis=0)
else:
    df = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list)]

print(df)
df['last_updated_churn'] = df['last_updated_churn'].astype(str).str.strip().astype(int)
last_updated_churn_values = input(f"Select required churn: {df['last_updated_churn'].unique()}") # Replace with actual multiplechoice user input
last_updated_churn_list = [int(x) for x in last_updated_churn_values.split(',')]
df = df.loc[df['last_updated_churn'].isin(last_updated_churn_list)]

print(df)
job_title_filter = False # take user input here as a checkbox, keep it initially disabled
if job_title_filter:
    job_title_values = input(f"Select job title: {df['job_title'].unique()}") # Replace with actual multiplechoice user input
    job_title_list = job_title_values.split(',')
    df = df.loc[df['job_title'].isin(job_title_list)]

job_level_filter = False # take user input here as a checkbox, keep it initially disabled
if job_level_filter:
    job_level_values =  input(f"Select job level: {df['job_level'].unique()}")# Replace with actual multiplechoice user input
    job_level_list = job_level_values.split(',')
    df = df.loc[df['job_level'].isin(job_level_list) | df['job_level'].isnull()]

job_function_filter = False # take user input here as a checkbox, keep it initially disabled
if job_function_filter:
    job_function_values = input(f"Select job function: {df['job_function'].unique()}") # Replace with actual multiplechoice user input
    job_function_list = job_function_values.split(',')
    df = df.loc[df['job_function'].isin(job_function_list)]

employee_size_filter = False # take user input here as a checkbox, keep it initially disabled
if employee_size_filter:
    employee_size_value = input(f"Select employee size: {df['employee_size'].unique()}") # Replace with actual multiplechoice user input
    employee_size_list = employee_size_value.split(',')
    df = df.loc[df['employee_size'].isin(employee_size_list)]

industry_filter = False # take user input here as a checkbox, keep it initially disabled
if industry_filter:
    industry_value = input(f"Select industry: {df['industry'].unique()}") # Replace with actual multiplechoice user input
    industry_list = industry_value.split(',')
    df = df.loc[df['industry'].isin(industry_list)]

priority_2 = False # take user input here as a checkbox, keep it initially disabled
if priority_2:
    priority_2_value = input(f"Select priority: {df['priority'].unique()}") # Replace with actual multiplechoice user input
    priority_2_list = priority_2_value.split(',')
    df = df.loc[df['priority'].isin(priority_2_list)]

po = False # take user input here as a checkbox, keep it initially disabled
tag = False # take user input here as a checkbox, keep it initially disabled
tal_list = False # take user input here as a checkbox, keep it initially disabled

print(df)

df.sort_values(by='last_updated_churn', inplace=True)

all_headers = master_df.columns.tolist()
selected_columns = ['member_id', 'email', 'first_name', 'last_name', 'job_title', 'job_level', 'job_function', 'company', 'address', 'city', 'state', 'country', 'zip', 'phone', 'alternate_no', 'ext', 'time_zone', 'employee_size', 'company_revenue', 'industry', 'priority', 'owner', 'original_owner', 'website', 'project']
# extra_columns = [header for header in all_headers if header not in selected_columns]
df = df[selected_columns]

count_of_websites = True # take user input here as a checkbox, keep it initially disabled
if count_of_websites:
    df['day before yesterday websites'] = df.groupby('website')['website'].transform('count')
    day_before_yesterday_websites = input(f"Select count: {df['day before yesterday websites'].unique()}") #Take multiplechoice user inout here
    day_before_yesterday_websites_required = [int(x) for x in day_before_yesterday_websites.split(',')]
    df = df[df['day before yesterday websites'].isin(day_before_yesterday_websites_required)]

print(df)

count_of_companies = True # take user input here as a checkbox, keep it initially disabled
if count_of_companies:
    df['day before yesterday companies'] = df.groupby('company')['company'].transform('count')
    day_before_yesterday_companies = input(f"Select count: {df['day before yesterday companies'].unique()}")
    day_before_yesterday_companies_required = [int(x) for x in day_before_yesterday_companies.split(',')] #Take multiplechoice user inout here
    df = df[df['day before yesterday companies'].isin(day_before_yesterday_companies_required)]

df = df.drop_duplicates(subset=['phone'], keep="first")

print(df)

df = df[~df['website'].isin(websites)]
df = df[~df['company'].isin(companies)]
print(df)

today_date = pd.Timestamp.today().strftime('%y%m%d')
date_member_id_df = pd.DataFrame(columns=['date_member_id'])
date_member_id_df['date_member_id']= df['member_id'].astype(str) + '.' + today_date
# empty_df =pd.DataFrame(columns = extra_columns)

df = pd.concat([date_member_id_df, df], axis=1)

print(df)


df.to_excel(r'/home/vandita/Documents/BI voice/30 April/Ring_For_Business_30April.xlsx', index=False)


#All  : 'Member ID','Email','First Name','Last Name','Job Title','Job Level','Job Function','Company','Address','City','State','Country','Zip','Phone','Alternate No','Ext','Time Zone','Employee Size','Company Revenue','Industry','Priority','Owner','Original Owner','Website','Project','Day before yesterday'
#KFBCA: Yesterday   Churn	Pool	Disposition	Group	Today	02/02/2023	Legents	Match	Domain	Dmn	Project 13
#ABENT: Yesterday	Churn	Pool	Disposition	Group	Today	02/02/2023	Legents	Match	Domain	Dmn	Project 13	Project 13	Project 13	Project 13	Project 13	Project 13	Project 13	Project 13	Project 13	Project 13
#ProCa: Yesterday   Churn	Pool	Disposition	Group	Today	02/02/2023	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents	Legents
#Elatc: Yesterday	Churn	Pool	Disposition	Group	Today	02/02/2023	valid_invalid	last_updated_churn	last_updated_pool	last_updated_disposition	last_updated_group	last_updated_agent	last_updated_date	last_connected_no	last_updated_group1	tal_account_id_sfdc	priority2	tag	tal_list	suppressed	sales_subvertical	sales_l2_subvertical	po
###RFB: Yesterday   Churn	Pool	Disposition	Group	Today	DF	valid_invalid	last_updated_churn	last_updated_pool	last_updated_disposition	last_updated_group	last_updated_agent	last_updated_date	last_connected_no	last_updated_group1	tal_account_id_sfdc	priority2	tag	tal_list	suppressed	sales_subvertical	sales_l2_subvertical	po	maxout
#HungR: Yesterday   Churn	Pool	Disposition	Group	Today	DF	valid_invalid	last_updated_churn	last_updated_pool	last_updated_disposition	last_updated_group	last_updated_agent	last_updated_date	last_connected_no	last_updated_group1	tal_account_id_sfdc	priority2	tag	tal_list	suppressed	sales_subvertical	sales_l2_subvertical	po	maxout	job_level

# iA_ Elastic CS_Oct 2023
# Workable,Unused,None
# 2024-04-23
# Workable,Unused
# Gatekeeper,No Answer,Voicemail,Voicemail - Prospect,Performance Hangup,Callback,Busy
# 0,1,2,3,4,5
# nan,Voicemail,No Answer,Performance Hangup,Not Available - Try Again