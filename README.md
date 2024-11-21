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

## Installation:

To install Cherpy, use:

```bash
pip install cherpy
```

## Library usage:

### Create client credentials from config

```python

from cherpy.auth import config_from_env
from cherpy.main import search_object

# create client using env variable which contains the config file path
client = config_from_env("cherwell_dev")

# search for any incident object name, limit to 10 (0 for all)
search_object(client, object_name="Incident", pageSize=10)

# search for any incident containing the text desktop and returning the fields IncidentID and ownedbyteam 
search_object(client, object_name="Incident", fields=["IncidentID", "ownedbyteam"], search_string="desktop",
              pageSize=10)

```

### Windows Command Line Usage:

# Cherpy CLI Usage Guide

Cherpy is a command-line tool for interacting with the Cherwell API. Here's how to use each command:

## Common Options

All commands support these common options:

- `-e, --env`: Environment variable containing config path (default: "cherpy_config")
- `--object-name`: Name of the Cherwell object

## Commands

### Search

Search for Cherwell objects.

```bash
# Basic search returning specific fields
csm search --env cherwell_dev --object-name Incident FirstName LastName Status

# Search with text filter and pagination
csm search --env cherwell_dev --object-name Incident -s "printer issue" -ps 100 -pg 1

# Search and save status and description for all incidents to a file
csm search --object-name Incident -o output.csv Status Description
```

### Create

Create new Cherwell records.

```bash
# Create from input file
csm create --env cherwell_config --object-name Incident -input-path data.csv

# Create with file dialog
csm create --env cherwell_config --object-name Incident -ask-file

# Create with direct key-value pairs
csm create --env cherwell_config --object-name Incident Description="New Issue" Status="New"
```

### Update

Update existing Cherwell records (requires RecId field in input data).

```bash
# Update from file
csm update --object-name Incident --input-path updates.csv

# Update using file dialog
csm update --object-name Incident -a
```

### Delete

Delete Cherwell records in batches.

```bash
# Delete with default chunk size (300)
csm delete --object-name Incident

# Delete with custom chunk size
csm delete --object-name Incident --chunk-size 500
```

### Get Schema

Retrieve schema information for Cherwell objects.

```bash
# Get schema and display in console
csm get-schema --object-name Incident

# Save schema to file
csm get-schema --object-name Incident -o schema.txt
```

### OneStep Operations

#### Get OneStep

Get information about a OneStep automation.

```bash
# Get OneStep info
csm get-onestep --object-name Incident -on "ProcessIncident" -sc "Global"
```

#### Run OneStep

Execute a OneStep automation.

```bash
# Run OneStep
csm run-onestep --object-name Incident -on "ProcessIncident" -sc "Global"
```

## Example Workflow

```bash
# 1. Check object schema
csm get-schema --object-name Incident -o incident_schema.txt

# 2. Search for existing incidents
csm search --object-name Incident -s "printer" Status Description Owner

# 3. Create new incidents
csm create --object-name Incident --input-path new_incidents.csv

# 4. Update incidents
csm update --object-name Incident --input-path incident_updates.csv

# 5. Run a OneStep process
csm run-onestep --object-name Incident -on "ProcessIncident"
```

Note: All commands will prompt for the environment variable and object name if not specified
