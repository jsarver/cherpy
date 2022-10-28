## Overview

Cherpy is an API wrapper to provide an easy way use the rest api for the Cherwell platform

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

# create client using env variable which contains the config file path
client = config_from_env("cherwell_dev")

## token created
client.login()

```


