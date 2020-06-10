import dataiku
import logging
from dataiku.customrecipe import *
from hubspot import get_contacts, write_data, get_companies

logger = logging.getLogger(__name__)

output_names = get_output_names_for_role('output')
output_name = output_names[0]
output = dataiku.Dataset(output_name) 

api_key = get_recipe_config()['hapikey']
object_name = get_recipe_config()['object_name']
format_output = get_recipe_config()['format']
properties_type = get_recipe_config()['properties_type']
list_input = get_recipe_config()['property_names']

if (object_name == 'contacts'):
    results = get_contacts(api_key, properties_type, list_input)
else:
    results = get_companies(api_key, properties_type, list_input)

logger.info(str(len(results)) + " " + object_name + " downloaded")    
write_data(results, output, format_output)