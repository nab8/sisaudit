#!/usr/bin/env python3
"""This file queries the SIS API for equipment attributes."""
from main import fetch_sis_api, convert_attribute_list, get_nested_item, Device
import config
import math
import argparse
import json

# Take inputs
parser = argparse.ArgumentParser(
    description='Fetch a specified attribute from the SIS equipment API'
)
parser.add_argument("-o", "--ownercode", required=True,
                    help='Specify ownercode, ex UW, \
                    multiple ownercodes can be comma seperated'
                    )
parser.add_argument("-m", "--model", required=True,
                    help='Specify model, ex CENTAUR or "AIRLINK ES450", \
                    multiple models can be comma seperated'
                    )
parser.add_argument("-a", "--attribute", required=True,
                    help="Specify attribute, ex 'equipips/0/ipv4address' or \
                    'equipattribs/0/settingvalue'"
                    )
parser.add_argument("-s", "--state", default='both',
                    help="State, should be one of present, \
                    absent, or both; default both"
                    )
parser.add_argument("-f", "--format", default='raw',
                    help="Format, should be one of raw, csv, \
                    or json; default raw"
                    )
args = parser.parse_args()

# Process arguements & prep equipment list
attribute = convert_attribute_list(args.attribute)
models = args.model.split(",")
ownercode = args.ownercode
equipment = {}

# For each model fetch attribute
for model in models:
    # Populate devices
    device_count_fetch = fetch_sis_api(
        'equipment',
        {
            'ownercode': ownercode,
            'modelname': model,
            'page[size]': 1
            }
        )
    device_count = device_count_fetch['meta']['pagination']['count']
    device_pages = math.ceil(device_count/config.page_size)
    i = 1
    # Fetch each page
    while i <= device_pages:
        device_fetch = fetch_sis_api(
            'equipment',
            {
                'ownercode': ownercode,
                'modelname': model,
                'page[number]': i
                }
            )
        i += 1
        for device in device_fetch['data']:
            # Check for a lookup code
            try:
                lookupcode = (device['relationships']['equipinstalls']
                                    ['data'][0]['lookupcode'])
            except(IndexError, TypeError):
                lookupcode = "No_Location"
            # Check for attribute
            try:
                device_attribute = get_nested_item(device, attribute)
            except IndexError:
                device_attribute = ""
            if (
                    args.state.lower() == "both" or
                    args.state.lower() == "present" and device_attribute != ""
                    ):
                equipment[device["id"]] = Device(
                    id=device["id"],
                    model=model,
                    lookupcode=lookupcode,
                    host_name=lookupcode+"_"+model.replace(" ", "_"),
                    attribute=device_attribute,
                    url=device['links']['self']
                    )
            elif args.state.lower() == "absent" and device_attribute == "":
                equipment[device["id"]] = Device(
                    id=device["id"],
                    model=model,
                    lookupcode=lookupcode,
                    host_name=lookupcode+"_"+model.replace(" ", "_"),
                    attribute=device_attribute,
                    url=device['links']['self']
                    )

# Output based on preferred format
if args.format == "raw":
    for device in equipment:
        print(equipment[device].__dict__)
elif args.format == "json":
    output = '{'
    output += '"  equipment":['
    for device in equipment:
        if device != list(equipment)[-1]:
            output += json.dumps(equipment[device].__dict__)+","
        else:
            output += json.dumps(equipment[device].__dict__)
    output += '  ]'
    output += '}'
    print(json.dumps(json.loads(output), indent=2))
elif args.format == "csv":
    print("id,model,lookupcode,host_name,attribute,url")
    for device in equipment:
        print(equipment[device].id+",", end="")
        print(equipment[device].model+",", end="")
        print(equipment[device].lookupcode+",", end="")
        print(equipment[device].host_name+",", end="")
        print('"'+equipment[device].attribute+'",', end="")
        print(equipment[device].url)
