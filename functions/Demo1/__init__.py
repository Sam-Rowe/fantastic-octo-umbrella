import logging
import requests

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # get the current generation mix from the carbonintensity api - https://api.carbonintensity.org.uk/regional/england
    # and return the data as a json object
    generationmix = requests.get('https://api.carbonintensity.org.uk/regional/england').json()

    # extract the data key from the json object
    generationmix_data = generationmix['data'][0]['data'][0]['generationmix']

    # create a dictionary to hold generationmix data 
    # where the data is [{'fuel': 'biomass', 'perc': 5.8}, {'fuel': 'coal', 'perc': 1.5}, {'fuel': 'imports', 'perc': 16.2}, {'fuel': 'gas', 'perc': 52.5}, {'fuel': 'nuclear', 'perc': 8.9}, {'fuel': 'other', 'perc': 0}, {'fuel': 'hydro', 'perc': 0.4}, {'fuel': 'solar', 'perc': 2.4}, {'fuel': 'wind', 'perc': 12.3}]
    generationmix_dict = {}
    for generationmix_data_item in generationmix_data:
        generationmix_dict[generationmix_data_item['fuel']] = generationmix_data_item['perc']
    
    # create a pie chart fromt the generationmix data using the matplotlib library
    import matplotlib.pyplot as plt
    plt.pie(generationmix_dict.values(), labels=generationmix_dict.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('Generation Mix')
    plt.savefig('/tmp/generationmix.png')
    plt.close()


    # read /tmp/generationmix.png as a byte array
    with open('/tmp/generationmix.png', 'rb') as f:
        # read the file into a byte array  
        img_bytes = f.read()
        # return the bytearray as a func.HttpResponse
        return func.HttpResponse(img_bytes, mimetype='image/png')


        
