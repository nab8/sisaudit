import requests
import config
import json
from functools import reduce

class Device:
	def __init__(self, id, model, lookupcode, host_name, attribute, url):
		self.id = id
		self.model = model
		self.lookupcode = lookupcode
		self.host_name = host_name
		self.attribute = attribute
		self.url = url

def fetch_sis_api(path, params = {}, env = config.env):
	url = "https://anss-sis.scsn.org/"+env+"/api/v1/"+path
	headers = {'Authorization': 'Bearer '+config.api_key,}
	if params.get('page[size]') is None:
		params['page[size]'] = config.page_size
	r = requests.get(url, headers = headers, params=params)
	res = r.json()
	return(res)

def convert_attribute_list(attribute):
	attribute = attribute.split('/')
	if attribute[0] != "attributes":
		attribute.insert(0, "attributes")
	for i in range(len(attribute)):
	    try:
	        attribute[i] = int(attribute[i])
	    except ValueError:
	        pass
	return(attribute)

# From https://codereview.stackexchange.com/a/224688
def get_nested_item(data, keys):
    return reduce(lambda seq, key: seq[key], keys, data)	