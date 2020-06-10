import json, logging
from pandas.io.json import json_normalize

logger = logging.getLogger(__name__)

def write_data(list_jsons, output_dataset, format_output):  
    if format_output == 'JSON':
        writer = output_dataset.get_writer()
        output_dataset.write_schema([{"name": "object","type": "string"}])
        for list_objects in list_jsons:
            print(list_objects)
            writer.write_row_array([json.dumps(list_objects)])
        logger.info("Writing to output")

        writer.close()
    elif format_output == 'Readable with columns':
        output_result = json_normalize(list_jsons)
        output_dataset.write_with_schema(output_result)
        logger.info("Writing to output")
