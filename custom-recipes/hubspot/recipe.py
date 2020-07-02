from dataiku import pandasutils as pdu
import pandas as pd, numpy as np
import re
import dataiku
import dataikuapi
from dataiku import api_client as client
from dataiku.core.sql import SQLExecutor2
import json, time, requests
import logging
from dataiku.customrecipe import *
import urllib
from pandas.io.json import json_normalize
from hubspot import get_contacts, write_data_json, write_data_columns, get_companies

logger = logging.getLogger(__name__)

output_names = get_output_names_for_role('output')
output_name = output_names[0]
output = dataiku.Dataset(output_name) 

api_key = get_recipe_config()['hapikey']
object_name = get_recipe_config()['object_name']
format_output = get_recipe_config()['format']
properties_type = get_recipe_config()['properties_to_retrieve']
list_input = get_recipe_config()['custom_properties_list']
counter = 0

if format_output == 'JSON':
    writer = output.get_writer()
    logger.info( "Writer opened")
    if (object_name == 'contacts'):
        for contact in get_contacts(api_key, properties_type, list_input):
            write_data_json(writer, contact, output, format_output)
            counter += 1
    else:
        for company in get_companies(api_key, properties_type, list_input):
            write_data_json(writer, company, output, format_output)
            counter += 1
    writer.close()
    logger.info( "Writer closed")
    
    
elif format_output == 'Readable with columns':    
    if(object_name == 'contacts'):
        for contact in get_contacts(api_key, properties_type, list_input):
            write_data_columns(contact, output, format_output)
            counter += 1
    else:
        for company in get_companies(api_key, properties_type, list_input):
            write_data_columns(company, output, format_output)
            counter += 1

logger.info(str(counter) + " " + object_name + " downloaded")