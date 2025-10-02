import requests
import pandasdmx as sdmx

#crime data

# data api

dataflowIdentifier = "DEATHS_AGESPECIFIC_OCCURENCEYEAR"
    # get all dataflowIds
url = f"https://data.api.abs.gov.au/rest/data/{dataflowIdentifier}/all"

params = {
    "startPeriod":"2024",
    "format":"jsondata"
}

response = requests.get(url = url, params = params)

data = response.json()

print(data['data']['dataSets'][0].keys())

#print(data['data']['structures'][0])
# structures pathway
#print(data.get('data').get('structures')[0].keys())

# data pathway
#print(data.get('data').get('dataSets')[0].keys())

#print(data.get('data').get('structures')[0].get('dataSets'))
# params = {
#     "format":"jsondata"
# }

# headers = {
#     "accept":"application/vnd.sdmx.data+json"
# }





# print(response.request.body)
# print(response.request.headers)

#print(response.json)

# indicator api

# time series directory api