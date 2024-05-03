from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import psycopg2
import basic2
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
    campaign_names = fetch_campaign_names()

    if request.method == 'GET':

        # Prepare the response data
        form_data1 = [
            {'label': 'Campaign_Name', 'options': campaign_names, 'type': 'select', 'default': None, 'child': None, 'parent': 'Campaign_Name'},
            {'label': 'Maxout', 'options': [], 'type': 'radio', 'default': False, 'child': 'maxout', 'parent': 'Maxout'},
            {'label': 'maxout', 'options': [1, 2, 3, 4, 5], 'type': 'select', 'default': False, 'child': None, 'parent': 'Maxout'}
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

        form_data = [
            {'label': 'Campaign_Name',
            'options': [campaign_name],
            'type': 'select',
            'default': campaign_name,
            'parent': 'Campaign_Name',
            'child': None},
            {'label': 'maxout',
             'options': [maxout_toggle],
             'type' : 'radio',
             'default': maxout_toggle,
             'parent': 'maxout',
             'child':'maxout_value'},
            {'label':'maxout_value',
             'options': [maxout_input],
             'type': 'select',
             'default': maxout_input,
             'parent':'maxout',
             'child': None},
            {'label' : 'last_updated_group1_value', 
            'options': df['last_updated_group1'].unique().tolist(), 
            'type': 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_group1_value',
            'child' : None},

            {'label' : 'last_updated_date_value', 
            'options' : df['last_updated_date'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_date_value',
            'child' : None},

            {'label' : 'last_updated_group_value', 
            'options' : df['last_updated_group'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_group_value',
            'child' : None},

            {'label' : 'last_updated_disposition_value', 
            'options' : df['last_updated_disposition'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_disposition_value',
            'child' : None},

            {'label' : 'last_updated_churn_value', 
            'options' : df['last_updated_churn'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'last_updated_churn_value',
            'child' : None},

            {'label' : 'job_title_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'job_title_filter',
            'child' : 'job_title_value'},
            {'label' : 'job_title_value', 
            'options' : df['job_title'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'job_title_filter',
            'child' : None},

            {'label' : 'job_level_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'job_level_filter',
            'child' : 'job_level_value'},
            {'label' : 'job_level_value', 
            'options' : df['job_level'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'job_level_filter',
            'child' : None},

            {'label' : 'job_function_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'job_function_filter',
            'child' : 'job_function_value'},
            {'label' : 'job_function_value', 
            'options' : df['job_function'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'job_function_filter',
            'child' : None},

            {'label' : 'employee_size_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'employee_size_filter',
            'child' : 'employee_size_value'},
            {'label' : 'employee_size_value', 
            'options' : df['employee_size'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'employee_size_filter',
            'child' : None},

            {'label' : 'industry_filter', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'industry_filter',
            'child' : 'industry_value'},
            {'label' : 'industry_value', 
            'options' : df['industry'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'industry_filter',
            'child' : None},

            {'label' : 'priority2', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'priority2',
            'child' : 'priority2_value'},
            {'label' : 'priority2_value', 
            'options' : df['priority2'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'priority2',
            'child' : None},
            
            {'label' : 'po', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'po',
            'child' : 'po_value'},
            {'label' : 'po_value', 
            'options' : df['po'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'po',
            'child' : None},

            {'label' : 'tag', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'tag',
            'child' : 'tag_value'},
            {'label' : 'tag_value', 
            'options' : df['tag'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'tag',
            'child' : None},

            {'label' : 'tal_list', 
            'options' : [], 
            'type' : 'radio', 
            'default' : None, 
            'parent' : 'tal_list',
            'child' : 'tal_list_value'},
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
            'parent' : 'count_of_websites',
            'child' : 'day_before_yesterday_websites'},
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
            'parent' : 'count_of_companies',
            'child' : 'day_before_yesterday_companies'},
            {'label' : 'day_before_yesterday_companies', 
            'options' : df['day_before_yesterday_companies'].unique().tolist(), 
            'type' : 'multiselect', 
            'default' : None, 
            'parent' : 'count_of_companies',
            'child' : None},
        ]
        
        
        return render(request, 'home-complex.html', {'form_data': form_data})
    
def home_complex(request):
    if request.method == 'POST':
        campaign_name = request.POST.get('Campaign_Name-input')
        maxout = request.POST.get('maxout-input')
        maxout_list = request.POST.get('maxout_value-input')
        last_updated_group1_list = request.POST.get('last_updated_group1_value-input')
        last_updated_date_list = request.POST.get('last_updated_date_value-input')
        last_updated_group_list = request.POST.get('last_updated_group_value-input')
        last_updated_disposition_list = request.POST.get('last_updated_disposition_value-input')
        last_updated_churn_list = request.POST.get('last_updated_churn_value-input')
        job_title_filter = request.POST.get('job_title_filter-input')
        job_title_list = request.POST.get('job_title_value-input')
        job_level_filter = request.POST.get('job_level_filter-input')
        job_level_list = request.POST.get('job_level_value-input')
        job_function_filter = request.POST.get('job_function_filter-input')
        job_function_list = request.POST.get('job_function_value-input')
        employee_size_filter = request.POST.get('employee_size_filter-input')
        employee_size_list = request.POST.get('employee_size_value-input')
        industry_filter = request.POST.get('industry_filter-input')
        industry_list = request.POST.get('industry_value-input')
        po = request.POST.get('po-input')
        po_list = request.POST.get('po_value-input')
        priority2 = request.POST.get('priority2-input')
        priority2_list = request.POST.get('priority2_value-input')
        tag = request.POST.get('tag-input')
        tag_list = request.POST.get('tag_value-input')
        tal_list = request.POST.get('tal_list-input')
        tal_list_list = request.POST.get('tal_list_value-input')
        count_of_websites = request.POST.get('count_of_websites-input')
        day_before_yesterday_websites_required = request.POST.get('day_before_yesterday_websites-input')
        count_of_companies = request.POST.get('count_of_companies-input')
        day_before_yesterday_companies_required = request.POST.get('day_before_yesterday_companies-input')

        # print everything

        master_df = fetch_campaign_data(campaign_name)

        final_df = basic2.process(
            master_df,
            campaign_name,
            maxout,
            maxout_list,
            last_updated_group1_list,
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
            day_before_yesterday_companies_required,
        )

        return render(request, 'home-complex.html', {})



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