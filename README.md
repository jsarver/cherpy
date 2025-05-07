## Overview

Cherpy is an API wrapper library to provide an easy way use the Cherwell rest API. It can be used for new scripts or
simply used via the command line.

You can do the following:

* Create and update objects
* Search for objects
* Delete objects
* Get schema information
* Search for a onestep
* Call a onestep

## Installation:

To install Cherpy, use:

```bash
pip install cherpy
```

# Quick start Guide

Before you can start interacting with cherwell you will need to setup a config file that contains the necessary info

## Configuration Example

### Below is an example config file to authenticate to cherwell

```yaml
    "auth_mode": "LDAP",
    "client_id": "<client id>",
    "grant_type": "password",
    "host": "https://<url>/CherwellAPI",
    "password": "<password>",
    "user": "domain\<userid>"
```

You can save the above file to a any location but a suggested location is %userprofile%/.cherpy/cherpy_config.yaml

## Common tasks

### Search for Cherwell objects.

```bash
# Basic search returning specific fields
csm search --env cherwell_dev --object-name --output-path "c:\myexports\incidents.csv" Incident IncidentID Status Ownedbyteam

# Search for the first 100 tickets with the text "printer issue" them
csm search --env cherwell_dev --object-name Incident -s "printer issue" -page-size 100

```

### Create

Create new Cherwell records.

```bash
# Create from input file
csm create --env cherwell_config --object-name Incident -input-path data.csv

# The convenience flag --ask-file can be used if you prefer to just browser for the file you want to import
csm create --env cherwell_config --object-name Incident -ask-file

# Create with direct key-value pairs
csm create --env cherwell_config --object-name Incident Description="New Issue" Status="New"
```

### Update

Update existing Cherwell records (requires RecId field in input data).

```bash
# Update from file
csm update --env cherwell_config --object-name Incident -input-path update_incidents.csv

# Update using file dialog
csm update --env cherwell_config --object-name Incident -ask-file
```

### Delete

Delete Cherwell records in batches.

```bash
# Delete with default chunk size (300)
csm delete --env cherwell_config --object-name Incident --input-path delete_incidents.csv

# Delete all records in the file with in batches of 100
csm delete --env cherwell_config --object-name Incident --input-path delete_incidents.csv --chunk-size 100
```

### Get Schema

Retrieve schema information for Cherwell objects.

```bash
# Get schema and display in console
csm get-schema --object-name Incident

# Save schema to file
csm get-schema --object-name Incident --output-path schema.txt
```

### OneStep Operations

#### Get OneStep

Get information about a OneStep automation. More of a helper tool to confirm that you have the correct OneStep before
running it.

```bash
>>csm get-onestep --env cherpy_dev --object-name configserver -on "Retire Server"
  2024-11-26 12:37:13.939 | INFO     | cherpy.cli:get_onestep_cli:75 - Current Env: cherpy_dev
  2024-11-26 12:37:13.943 | INFO     | cherpy.cli:get_onestep_cli:76 - Searching for Retire Server in Global for Association: configserver
  2024-11-26 12:37:13.948 | INFO     | cherpy.runonestep:get_object_summary:38 - Getting object summary for configserver
  2024-11-26 12:37:14.840 | INFO     | cherpy.runonestep:_recurse_onestep:29 - Found it!
  2024-11-26 12:37:14.844 | INFO     | cherpy.runonestep:get_onestep:76 - Found this onestep Retire Server
  2024-11-26 12:37:14.849 | INFO     | cherpy.runonestep:get_onestep:77 - {'association': '93dada9f640056ce1dc67b4d4bb801f69104894dc8',
   'description': '',
   'displayName': 'Retire Server',
   'galleryImage': '',
   'id': '94b43f85e5ce44034265864b12b22aecd83ebe0f10',
   'links': [],
   'localizedScopeName': 'Global',
   'name': 'Call Delete Duplicate Servers',
   'parentFolder': '',
   'parentIsScopeFolder': True,
   'scope': 'Global',
   'scopeOwner': '(None)',
   'standInKey': 'DefType:OneStepDef#Scope:Global#Id:94b43f85e5ce44034265864b12b22aecd83ebe0f10#Owner:93dada9f640056ce1dc67b4d4bb801f69104894dc8'}
```

#### Run OneStep

Execute a OneStep.

```bash
# Run a oneStep in the Incident association in the Global scope/folder
# Note: Onesteps that run against a search group are not searchable via the API. One workaround is a create a onestep 
# without a search group that calls the onestep with the search group
csm run-onestep --object-name Incident --onestep-name "Create Incident" --scope "Global"
```

## Library usage:

### Create client credentials from config

```python

from cherpy.auth import config_from_env
from cherpy.api import search_object

# create client using env variable which contains the config file path
client = config_from_env("cherwell_dev")

# search for any incident object name, limit to 10 (0 for all)
search_object(client, object_name="Incident", pageSize=10)

# search for any incident containing the text desktop and returning the fields IncidentID and ownedbyteam 
search_object(client, object_name="Incident", fields=["IncidentID", "ownedbyteam"], search_string="desktop",
              pageSize=10)

```
