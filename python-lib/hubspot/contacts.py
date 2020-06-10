import json, time, requests
import urllib

def get_contact_properties(apikey):
    get_all_properties_url = "https://api.hubapi.com/properties/v1/contacts/properties?"
    parameter_dict = {'hapikey': apikey}
    headers = {}
    parameters = urllib.urlencode(parameter_dict)
    get_url = get_all_properties_url + parameters
    r = requests.get(url= get_url, headers = headers)
    response_dict = json.loads(r.text)
    list_contacts_properties = [x[u'name'] for x in response_dict]
    return list_contacts_properties

def get_contacts(apikey, properties_type, list_input):
    limit = 100
    contact_list = []
    get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
    headers = {}
    if properties_type == 'Standard':
        contact_properties = []
        parameter_dict = {'hapikey': apikey, 'count': limit, 'property': contact_properties}
    elif properties_type == 'All':
        contact_properties = get_contact_properties(apikey)
        parameter_dict = {'hapikey': apikey, 'count': limit, 'property': contact_properties}
    elif properties_type == 'Custom':
        contact_properties = list_input
        parameter_dict = {'hapikey': apikey, 'count': limit, 'property': contact_properties}   
        
    # Paginate your request using offset
    has_more = True
    counter = 0
    while has_more:
        parameters = urllib.urlencode(parameter_dict, True)
        get_url = get_all_contacts_url + parameters
        r = requests.get(url= get_url, headers = headers)
        counter +=1
        response_dict = json.loads(r.text)
        has_more = response_dict['has-more']
        contact_list.extend(response_dict['contacts'])
        parameter_dict['vidOffset']= response_dict['vid-offset']
        if counter >= 90:
            time.sleep(12)
            counter = 0
    return contact_list