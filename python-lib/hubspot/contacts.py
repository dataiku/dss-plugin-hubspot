import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import json, time, requests
import urllib
from pandas.io.json import json_normalize
from constants import Constants

const = Constants()

def get_contact_properties(apikey):
    try:
        r = requests.get("https://api.hubapi.com/properties/v1/contacts/properties?", params = {'hapikey': apikey})
    except:
        if (r.status_code != 200 and method == 'get'):
            raise Exception('API error when calling {}, error code {}. Returned response : {}'.format(r.url, r.status_code, r.json()))
    response_dict = r.json()
    list_contacts_properties = [x[u'name'] for x in response_dict]
    return list_contacts_properties

def get_contacts(apikey, properties_type, list_input):
    if properties_type == 'Standard':
        parameter_dict = {'hapikey': apikey, 'count': const.CONTACTS_LIMIT, 'property': contact_properties}
    elif properties_type == 'All':
        contact_properties = get_contact_properties(apikey)
        parameter_dict = {'hapikey': apikey, 'count': const.CONTACTS_LIMIT, 'property': contact_properties}
    elif properties_type == 'Custom':
        contact_properties = list_input
        parameter_dict = {'hapikey': apikey, 'count': const.CONTACTS_LIMIT, 'property': contact_properties}   
    has_more = True
    counter = 0
    while has_more:
        try:
            r = requests.get("https://api.hubapi.com/contacts/v1/lists/all/contacts/all?", params = parameter_dict)
        except:
            if (r.status_code != 200 and method == 'get'):
                raise Exception('API error when calling {}, error code {}. Returned response : {}'.format(r.url, r.status_code, r.json()))
        counter +=1
        response_dict = r.json()
        has_more = response_dict['has-more']
        yield response_dict['contacts']
        parameter_dict['vidOffset']= response_dict['vid-offset']
        if counter >= 95:
            time.sleep(10)
            counter = 0