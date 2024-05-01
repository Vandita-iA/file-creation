from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import psycopg2

# Define your database connection parameters
DB_NAME = 'dev_voice'
DB_USER = 'postgres'
DB_PASSWORD = 'Password123*'
DB_HOST = '192.168.1.189'
DB_PORT = '5432'

def fetch_campaign_names():
    # Connect to the database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    # Run the query to fetch campaign names
    query = "SELECT DISTINCT campaign_name FROM public.data_distribution_master"
    with conn.cursor() as cursor:
        cursor.execute(query)
        campaign_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return campaign_names


def fetch_campaign_data(campaign_name):
    # Connect to the database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    # Run the query to fetch campaign data
    query = "SELECT * FROM public.data_distribution_master WHERE campaign_name = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (campaign_name,))
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
    conn.close()
    # Convert fetched data into a DataFrame
    df = pd.DataFrame(data)
    return df


def home_simple(request):
    if request.method == 'GET':
        campaign_names = fetch_campaign_names()

        # Prepare the response data
        form_data1 = [
            {'label': 'Campaign_Name', 'options': campaign_names, 'type': 'select', 'default': None, 'child': None, 'parent': 'Campaign_Name'},
            {'label': 'Maxout', 'options': [], 'type': 'radio', 'default': False, 'child': 'maxout', 'parent': 'Maxout'},
            {'label': 'maxout', 'options': [1, 2, 3, 4, 5], 'type': 'multiselect', 'default': False, 'child': None, 'parent': 'Maxout'}
        ]
        # print(form_data1)
        return render(request, 'home-simple.html', {'form_data': form_data1})
    
    if request.method == 'POST':

        campaign_name = request.POST.get('Campaign_Name-input')
        maxout_toggle = request.POST.get('Maxout-input')
        maxout_input = request.POST.get('maxout-input')

        master_df = fetch_campaign_data(campaign_name)

        if maxout_toggle == 'on':
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

        df['day_before_yesterday_websites']= df.groupby('website')['website'].transform('count')
        df['day_before_yesterday_companies'] = df.groupby('company')['company'].transform('count')

        response_data = [
            {'label' : 'last_updated_group1_values', 
            'options': df['last_updated_group1'].unique().tolist(), 
            'type': 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_group1_values',
            'child' : None},
            {'label' : 'last_updated_date_values', 
            'options' : df['last_updated_date'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_date_values',
            'child' : None},
            {'label' : 'last_updated_group_values', 
            'options' : df['last_updated_group'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_group_values',
            'child' : None},
            {'label' : 'last_updated_disposition_values', 
            'options' : df['last_updated_disposition'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_disposition_values',
            'child' : None},
            {'label' : 'last_updated_churn_values', 
            'options' : df['last_updated_churn'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_churn_values',
            'child' : None},
            {'label' : 'job_title_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'job_title_filter',
            'child' : 'job_title_values'},
            {'label' : 'job_level_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'job_level_filter',
            'child' : 'job_level_values'},
            {'label' : 'job_function_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'job_function_filter',
            'child' : None},
            {'label' : 'employee_size_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'employee_size_filter',
            'child' : 'employee_size_values'},
            {'label' : 'industry_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'industry_filter',
            'child' : 'industry_values'},
            # {'label' : 'priority_2', 
            # 'options' : [], 
            # 'type' : 'radio', 
            # 'default' : None, 
            # 'parent' : 'priority_2',
            # 'child' : 'priority_2_value'},
            {'label' : 'po', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'po',
            'child' : 'po_value'},
            {'label' : 'tag', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'tag',
            'child' : 'tag_value'},
            {'label' : 'tal_list', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'tal_list',
            'child' : 'la_list_value'},
            {'label' : 'job_title_value', 
            'options' : df['job_title'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'job_title_filter',
            'child' : None},
            {'label' : 'job_level_value', 
            'options' : df['job_level'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'job_level_filter',
            'child' : None},
            {'label' : 'job_function_value', 
            'options' : df['job_function'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'job_function_filter',
            'child' : None},
            {'label' : 'employee_size_value', 
            'options' : df['employee_size'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'employee_size_filter',
            'child' : None},
            {'label' : 'industry_value', 
            'options' : df['industry'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'industry_filter',
            'child' : None},
            # {'label' : 'priority_2_value', 
            # 'options' : df['priority_2'].unique().tolist(), 
            # 'type' : 'multiselect', 
            # 'default' : None, 
            # 'parent' : 'priority_2',
            # 'child' : None},
            {'label' : 'po_value', 
            'options' : df['po'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'po',
            'child' : None},
            {'label' : 'tag_value', 
            'options' : df['tag'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'tag',
            'child' : None},
            {'label' : 'tal_list_value', 
            'options' : df['tal_list'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'tal_list',
            'child' : None},
            {'label' : 'count_of_websites', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : '',
            'child' : None},
            {'label' : 'day_before_yesterday_websites', 
            'options' : df['day_before_yesterday_websites'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'count_of_websites',
            'child' : None},
            {'label' : 'count_of_companies', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : '',
            'child' : None},
            {'label' : 'day_before_yesterday_companies', 
            'options' : df['day_before_yesterday_companies'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'count_of_companies',
            'child' : None},
        ]
        return JsonResponse(response_data, safe=False)
        
        # return render(request, 'home-complex.html', {})

def index(request):
    if request.method == 'GET':
        # Step 1: Fetch Campaign Names
        campaign_names = fetch_campaign_names()

        # Prepare the response data
        form_data1 = [
            {'label': 'Campaign_Name', 
             'options': campaign_names, 
             'type': 'select', 
             'default': None, 
             'parent': 'Campaign_Name', 
             'child' : None},
            {'label': 'Maxout', 
            'options': [], 
            'type': 'radio', 
            'default': False, 
            'parent': 'Maxout',
            'child' : 'maxout'},
            {'label': 'maxout', 
            'options': [1, 2, 3, 4, 5], 
            'type': 'select', 
            'default': False, 
            'parent': 'Maxout',
            'child' : None}
        ]
        print(form_data1)
        return render(request, 'main.html', {'form_data': form_data1})

    elif request.method == 'POST':
        # Retrieve the selected Campaign Name from the request
        campaign_name = request.POST.get('campaign_name', '')

        # Step 2: Query the database for campaign data
        master_df = fetch_campaign_data(campaign_name)

        # Perform data filtering and manipulation
        websites = master_df.loc[master_df['last_updated_disposition'] == 'Lead For Qualification', 'website'].tolist()
        companies = master_df.loc[master_df['last_updated_disposition'] == 'Lead For Qualification', 'company'].tolist()
        df = master_df.loc[
            (master_df['dd'].isnull()) &
            (master_df['ab_user'].isnull()) &
            (master_df['maxout'].isnull()) &
            (master_df['dnc'].isnull()) &
            (master_df['suppressed'].isnull())].copy()
        df['project'] = df['campaign_name']

        # Prepare the response data for Step 4
        

        # return JsonResponse(response_data, safe=False)