import json, time, requests
import urllib

def get_company_properties(apikey):
    get_all_properties_url = "https://api.hubapi.com//properties/v1/companies/properties?"
    parameter_dict = {'hapikey': apikey}
    headers = {}
    parameters = urllib.urlencode(parameter_dict)
    get_url = get_all_properties_url + parameters
    r = requests.get(url= get_url, headers = headers)
    response_dict = json.loads(r.text)
    list_companies_properties = [x[u'name'] for x in response_dict]
    return list_companies_properties

def get_companies(apikey, properties_type, list_input):
    limit = 250 
    company_list = []
    headers = {}
    get_all_companies_url = "https://api.hubapi.com/companies/v2/companies/paged?"
    if properties_type == 'Standard':
        parameter_dict = {'hapikey': apikey, 'limit': limit}
    elif properties_type == 'All':
        company_properties = get_company_properties(apikey)
        parameter_dict = {'hapikey': apikey, 'limit': limit, 'properties': company_properties}
    elif properties_type == 'Custom':
        company_properties = list_input
        parameter_dict = {'hapikey': apikey, 'limit': limit, 'properties': list_input}
        
    # Paginate your request using offset
    has_more = True
    counter = 0
    while has_more:
        parameters = urllib.urlencode(parameter_dict, True)
        get_url = get_all_companies_url + parameters
        r = requests.get(url= get_url, headers = headers)
        counter += 1
        response_dict = json.loads(r.text)
        has_more = response_dict['has-more']
        company_list.extend(response_dict['companies'])
        parameter_dict['offset']= response_dict['offset']
        if counter >= 90:
            time.sleep(15)
            counter = 0
    return company_list