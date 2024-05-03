import pandas as pd
import psycopg2 as pg

# master_df = pd.read_excel('/home/vandita/Documents/BI voice/30 April/Masters/Ring_For_Business_Master_30_April.xlsx')
def process(master_df,
            campaign_name,
            maxout,
            maxout_list,
            last_updated_group1_list,
            last_updated_date_list,
            last_updated_group_list,
            last_updated_disposition_list,
            last_updated_churn_list,
            job_title_filter,
            job_title_list,
            job_level_filter,
            job_level_list,
            job_function_filter,
            job_function_list,
            employee_size_filter,
            employee_size_list,
            industry_filter,
            industry_list,
            po,
            po_list,
            priority2,
            priority2_list,
            tag,
            tag_list,
            tal_list,
            tal_list_list,
            count_of_websites,
            day_before_yesterday_websites_required,
            count_of_companies,
            day_before_yesterday_companies_required,):
    

    print(master_df)

    # take user input here as a checkbox, keep it initially disabled
    if maxout == 'on':
        master_df.loc[(master_df['last_updated_disposition'] == 'Lead For Qualification') & (master_df['maxout'].isna()), 'maxout'] = 'MAXOUT'

    websites = master_df.loc[master_df['last_updated_disposition'] == 'Lead For Qualification', 'website'].tolist()
    companies = master_df.loc[master_df['last_updated_disposition'] == 'Lead For Qualification', 'company'].tolist()

    master_df = master_df[~master_df['website'].isin(websites)]
    master_df = master_df[~master_df['company'].isin(companies)]
    print(master_df)

    df = master_df.loc[
        (master_df['dd'].isnull()) &
        (master_df['ab_user'].isnull()) &
        (master_df['maxout'].isnull()) &
        (master_df['dnc'].isnull()) &
        (master_df['suppressed'].isnull())].copy()

    df['project'] = df['campaign_name']

    print(df)
    
    #1
    last_updated_group1_list = [item.strip() for item in last_updated_group1_list.split(',')]
    if ('None' in last_updated_group1_list) or ('nan' in last_updated_group1_list):    
        df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list) | df['last_updated_group1'].isnull()]
    else:
        df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list)]
    
    #2
    print(df)
    last_updated_date_list = [item.strip() for item in last_updated_date_list.split(',')]
    df = df.loc[~df['last_updated_date'].isin(last_updated_date_list) | df['last_updated_date'].isnull()]

    #3
    print(df)
    last_updated_group_list = [item.strip() for item in last_updated_group_list.split(',')]
    if ('None' in last_updated_group_list) or ('nan' in last_updated_group_list):
        df = df.loc[df['last_updated_group'].isin(last_updated_group_list) | df['last_updated_group'].isnull()]
    else:
        df = df.loc[df['last_updated_group'].isin(last_updated_group_list)]

    #4
    print(df)
    df['last_updated_disposition'] = df['last_updated_disposition'].astype(str).str.replace("Not Available, Try Again", "Not Available - Try Again")
    last_updated_disposition_list = [item.strip() for item in last_updated_disposition_list.split(',')]
    if 'None' in last_updated_disposition_list or ('nan' in last_updated_disposition_list):
        last_updated_disposition_list.remove('None')
        df = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list) | df['last_updated_disposition'].isnull()]
    else:
        df = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list)]

    #5
    print(df)
    df['last_updated_churn'] = df['last_updated_churn'].astype(str).str.strip().astype(int)
    last_updated_churn_list = [item.strip() for item in last_updated_churn_list.split(',')]
    last_updated_churn_list = [int(x) for x in last_updated_churn_list]
    df = df.loc[df['last_updated_churn'].isin(last_updated_churn_list)]

    #6
    print(df)
    # take user input here as a checkbox, keep it initially disabled
    if job_title_filter == 'on':
        job_title_list = [item.strip() for item in job_title_list.split(',')]
        df = df.loc[df['job_title'].isin(job_title_list)]

    #7
    # take user input here as a checkbox, keep it initially disabled
    if job_level_filter == 'on':
        job_level_list = [item.strip() for item in job_level_list.split(',')]
        df = df.loc[df['job_level'].isin(job_level_list) | df['job_level'].isnull()]

    #8
     # take user input here as a checkbox, keep it initially disabled
    if job_function_filter == 'on':
        job_function_list = [item.strip() for item in job_function_list.split(',')]
        df = df.loc[df['job_function'].isin(job_function_list)]

    #9
     # take user input here as a checkbox, keep it initially disabled
    if employee_size_filter == 'on':
        employee_size_list = [item.strip() for item in employee_size_list.split(',')]
        df = df.loc[df['employee_size'].isin(employee_size_list)]

    #10
     # take user input here as a checkbox, keep it initially disabled
    if industry_filter == 'on':
        industry_list = [item.strip() for item in industry_list.split(',')]
        df = df.loc[df['industry'].isin(industry_list)]

    #11
     # take user input here as a checkbox, keep it initially disabled
    if priority2 == 'on':
        priority2_list = [item.strip() for item in priority2_list.split(',')]
        df = df.loc[df['priority'].isin(priority2_list)]

    #12
    po = False # take user input here as a checkbox, keep it initially disabled
    #13
    tag = False # take user input here as a checkbox, keep it initially disabled
    #14
    tal_list = False # take user input here as a checkbox, keep it initially disabled

    print(df)

    #sort
    df.sort_values(by='last_updated_churn', inplace=True)

    all_headers = master_df.columns.tolist()
    selected_columns = ['member_id', 'email', 'first_name', 'last_name', 'job_title', 'job_level', 'job_function', 'company', 'address', 'city', 'state', 'country', 'zip', 'phone', 'alternate_no', 'ext', 'time_zone', 'employee_size', 'company_revenue', 'industry', 'priority', 'owner', 'original_owner', 'website', 'project']
    # extra_columns = [header for header in all_headers if header not in selected_columns]
    df = df[selected_columns]

    # take user input here as a checkbox, keep it initially disabled
    if count_of_websites == 'on':
        df['day before yesterday websites'] = df.groupby('website')['website'].transform('count')
        day_before_yesterday_websites_required = [item.strip() for item in day_before_yesterday_websites_required.split(',')]
        day_before_yesterday_websites_required = [int(x) for x in day_before_yesterday_websites_required]
        df = df[df['day before yesterday websites'].isin(day_before_yesterday_websites_required)]

    print(df)

    # take user input here as a checkbox, keep it initially disabled
    if count_of_companies == 'on':
        df['day before yesterday companies'] = df.groupby('company')['company'].transform('count')
        day_before_yesterday_companies_required = [item.strip() for item in day_before_yesterday_companies_required.split(',')]
        day_before_yesterday_companies_required = [int(x) for x in day_before_yesterday_companies_required] #Take multiplechoice user inout here
        df = df[df['day before yesterday companies'].isin(day_before_yesterday_companies_required)]

    df = df.drop_duplicates(subset=['phone'], keep="first")

    print(df)

    

    today_date = pd.Timestamp.today().strftime('%y%m%d')
    date_member_id_df = pd.DataFrame(columns=['date_member_id'])
    date_member_id_df['date_member_id']= df['member_id'].astype(str) + '.' + today_date
    # empty_df =pd.DataFrame(columns = extra_columns)

    df = pd.concat([date_member_id_df, df], axis=1)

    print(df)


    return df

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