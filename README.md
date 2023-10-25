# Overview
This is a basic proof-of-concept for fetching an attribute from the SIS equipment API
## Config

### SIS Settings
* api_key - this is your SIS API key, see https://anss-sis.scsn.org/sis/api/v1/docs/#about-token-auth for instructions
* env - should either be sis (production) or sistest (testing)
* page_size - must be 500 or less; this is a tradeoff between the number of API calls and memory usage

## Running
The script has a handful of command arguements to make it simple to use for multiple purposes.

* -o OWNERCODE, --ownercode OWNERCODE; Specify ownercode, ex UW, multiple ownercodes can be comma seperated
* -m MODEL, --model MODEL; Specify model, ex CENTAUR or "AIRLINK ES450", multiple models can be comma seperated
* -a ATTRIBUTE, --attribute ATTRIBUTE; Specify attribute, ex 'equipips/0/ipv4address' or 'equipattribs/0/settingvalue'
* -s STATE, --state STATE; State, should be one of present, absent, or both; default both
* -f FORMAT, --format FORMAT; Format, should be one of raw, csv, or json; default raw

## Examples

```
# Get a list of UW CENTAURs & TITAN SMAs that have an IP address listed
./sisaudit.py -o UW -m "CENTAUR,TITAN SMA" -a "equipips/0/ipv4address" -s present 
# Get a list of UW Airlink ES450s that are missing IMEI addresses in JSON format
./sisaudit.py -o UW  -m "Airlink ES450" -a "equipattribs/0/settingvalue" -s absent -f json
# Get a list of UW, UO, USGS, & USGS-ESC-SEATTLE Xeta1-ELs & Xeta9-22DMLFCs serial numbers in CSV format
./sisaudit.py -o UW,USGS-ESC-SEATTLE,USGS,UO  -m "XETA1-EL,XETA9-22DMLFC" -a "serialnumber" -f csv
```