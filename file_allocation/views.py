# file_allocation/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import DataFilterForm
from .utils import fetch_campaign_names, fetch_data_from_database, filter_data_and_generate_excel

def filter_data(request):
    if request.method == 'POST':
        form = DataFilterForm(request.POST)
        if form.is_valid():
            campaign_name = form.cleaned_data.get('campaign_name')
            maxout = form.cleaned_data.get('maxout')
            last_updated_group1_list = form.cleaned_data.get('last_updated_group1_list')
            last_updated_date_list = form.cleaned_data.get('last_updated_date_list')
            last_updated_group_list = form.cleaned_data.get('last_updated_group_list')
            last_updated_disposition_list = form.cleaned_data.get('last_updated_disposition_list')
            last_updated_churn_list = form.cleaned_data.get('last_updated_churn_list')
            
            # Fetch data from the database based on the selected campaign_name
            master_df = fetch_data_from_database(campaign_name)
            
            # Filter data and generate Excel file
            file_path = filter_data_and_generate_excel(master_df, maxout, last_updated_group1_list, last_updated_date_list, last_updated_group_list, last_updated_disposition_list, last_updated_churn_list)
            
            return JsonResponse({'success': True, 'file_path': file_path})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Fetch initial options for the first field
        campaign_names = fetch_campaign_names()
        form = DataFilterForm()
        form.fields['campaign_name'].choices = [(name, name) for name in campaign_names]
        return render(request, 'filter_data.html', {'form': form})
