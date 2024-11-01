## Overview

Cherpy is an API wrapper library to provide an easy way use the Cherwell rest API. It can be used for new scripts or
simply used via
the command line.

This provides convenience for the following

* Create and update objects
* Search for objects
* Get schema information
* Delete objects
* Call a onestep

## Library usage:

### Create client credentials from config

```python

from cherpy.auth import config_from_env
from cherpy.main import search_object

# create client using env variable which contains the config file path
client = config_from_env("cherwell_dev")

## token created
client.login()

# search for any incident object object name, limit to 10 (0 for all)
search_object(client, object_name="Incident", pageSize=10)

# search for any incident containg the word desktop and rerning the fields IncidentID and ownedbyteam 
search_object(client, object_name="Incident", fields=["IncdientID", "ownedbyteam"], search_string="desktop",
              pageSize=10)

```

### Windows Command Line Usage:

```shell
#search for incident object and return the fields IncidentID and ownedbyteam
csm search -o Incident -env cherpy_dev -f IncidentID,ownedbyteam -s desktop -p 10 --output-file incident.csv

# search for incident object and return the fields IncidentID and ownedbyteam
csm search -o Incident -env cherpy_dev -f IncidentID,ownedbyteam -s desktop -p 10 --output-file incident.csv incidentid ownedbyteam

``` 