import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import json, time, requests, logging
import urllib
from pandas.io.json import json_normalize

def get_company_properties(apikey):
    try:
        r = requests.get("https://api.hubapi.com//properties/v1/companies/properties?", params = {'hapikey': apikey})
    except:
        if (r.status_code == 200 and method == 'get'):
            raise Exception('API error when calling {}, error code {}. Returned response : {}'.format(r.url, r.status_code, r.json()))
    response_dict = r.json()
    list_companies_properties = [x[u'name'] for x in response_dict]
    return list_companies_properties

def get_companies(apikey, properties_type, list_input):
    limit = 250 
    if properties_type == 'Standard':
        parameter_dict = {'hapikey': apikey, 'limit': limit}
    elif properties_type == 'All':
        company_properties = get_company_properties(apikey)
        parameter_dict = {'hapikey': apikey, 'limit': limit, 'properties': company_properties}
    elif properties_type == 'Custom':
        company_properties = list_input
        parameter_dict = {'hapikey': apikey, 'limit': limit, 'properties': list_input}
    has_more = True
    counter = 0
    while has_more:
        try:
            r = requests.get("https://api.hubapi.com/companies/v2/companies/paged?", params = parameter_dict)
        except:
            if (r.status_code == 200 and method == 'get'):
                raise Exception('API error when calling {}, error code {}. Returned response : {}'.format(r.url, r.status_code, r.json()))
        counter += 1
        response_dict = r.json()
        has_more = response_dict['has-more']
        yield response_dict['companies']
        parameter_dict['offset']= response_dict['offset']
        if counter >= 95:
            time.sleep(10)
            counter = 0