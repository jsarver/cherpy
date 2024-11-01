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

## Usage:

### Create client credentials from config

```python

from cherpy.auth import config_from_env
from cherpy.main import search_object

# create client using env variable which contains the config file path
client = config_from_env("cherwell_dev")

## token created
client.login()

# search for object using the id or the object name
search_object(client, object_name="Incident", fields=["IncdientID", "ownedbyteam"], search_string="desktop",
              pageSize=10)

```


