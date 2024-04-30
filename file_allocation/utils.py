# file_allocation/utils.py

import pandas as pd
import psycopg2 as pg

def fetch_campaign_names():
    try:
        connection = pg.connect(
            host="192.168.1.189",
            port="5432",
            database="dev_voice",
            user="postgres",
            password="Password123*"
        )
        print('Connection is On')
    except Exception as e:
        print(e)

    query = "SELECT DISTINCT campaign_name FROM public.data_distribution_master"
    cursor = connection.cursor()
    cursor.execute(query)
    campaign_name_list = cursor.fetchall()
    
    # Extract campaign names from the database
    campaign_names = [name[0] for name in campaign_name_list]
    
    connection.close()
    print('Connection closed')
    
    return campaign_names

def fetch_data_from_database(campaign_name):
    try:
        connection = pg.connect(
            host="192.168.1.189",
            port="5432",
            database="dev_voice",
            user="postgres",
            password="Password123*"
        )
        print('Connection is On')
    except Exception as e:
        print(e)

    query = f"SELECT * FROM public.data_distribution_master where campaign_name = '{campaign_name}'"
    master_df = pd.DataFrame()
    try:
        master_df = pd.read_sql_query(query, connection)
    except:
        print('Error: Unable to fetch data from the database')
    finally:
        connection.commit()
        connection.close()
        print('Connection closed')
    
    return master_df

def filter_data_and_generate_excel(master_df, maxout, last_updated_group1_list, last_updated_date_list, last_updated_group_list, last_updated_disposition_list, last_updated_churn_list):
    # Apply filters to the dataframe
    if maxout:
        master_df.loc[(master_df['last_updated_disposition'] == 'Lead For Qualification') & (master_df['maxout'].isna()), 'maxout'] = 'MAXOUT'

    df = master_df.loc[
        (master_df['dd'].isnull()) &
        (master_df['ab_user'].isnull()) &
        (master_df['maxout'].isnull()) &
        (master_df['dnc'].isnull()) &
        (master_df['suppressed'].isnull())].copy()

    if last_updated_group1_list:
        if 'None' in last_updated_group1_list:
            last_updated_group1_list.remove('None')
            df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list) | df['last_updated_group1'].isnull()]
        elif 'nan' in last_updated_group1_list:
            df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list) | df['last_updated_group1'].isnull()]
        else:
            df = df.loc[df['last_updated_group1'].isin(last_updated_group1_list)]

    if last_updated_date_list:
        df = df.loc[~df['last_updated_date'].isin(last_updated_date_list) | df['last_updated_date'].isnull()]

    if last_updated_group_list:
        if 'None' in last_updated_group_list:
            last_updated_group_list.remove('None')
            df = df.loc[df['last_updated_group'].isin(last_updated_group_list) | df['last_updated_group'].isnull()]
        elif 'nan' in last_updated_group_list:
            df = df.loc[df['last_updated_group'].isin(last_updated_group_list) | df['last_updated_group'].isnull()]
        else:
            df = df.loc[df['last_updated_group'].isin(last_updated_group_list)]

    df['last_updated_disposition'] = df['last_updated_disposition'].astype(str).str.replace("Not Available, Try Again", "Not Available - Try Again")

    if last_updated_disposition_list:
        if 'None' in last_updated_disposition_list:
            last_updated_disposition_list.remove('None')
            df = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list) | df['last_updated_disposition'].isnull()]
        elif 'nan' in last_updated_disposition_list:
            df1 = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list)]
            df2 = df.loc[df['last_updated_disposition'].isnull()]
            df = pd.concat([df1, df2], axis=0)
        else:
            df = df.loc[df['last_updated_disposition'].isin(last_updated_disposition_list)]

    if last_updated_churn_list:
        df['last_updated_churn'] = df['last_updated_churn'].astype(str).str.strip().astype(int)
        df = df.loc[df['last_updated_churn'].isin(last_updated_churn_list)]

    # Add other filters here

    # Sort dataframe
    df.sort_values(by='last_updated_churn', inplace=True)

    # Save filtered dataframe to Excel
    today_date = pd.Timestamp.today().strftime('%Y%m%d')
    file_path = f'/home/vandita/Documents/BI voice/29 April/Ring_for_Business_{today_date}.xlsx'
    df.to_excel(file_path, index=False)

    return file_path
