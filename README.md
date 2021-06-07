Cherpy is a set of API convenience methods for interacting with Cherwells Rest API

This tool allows you to do the following

Create and update objects

Search for objects

Get schema information

## Usage:

Creating an incident

# create client using env variable which contains the config file path

from cherpy.auth import config_from_env c = config_from_env("cherwell_dev")

# token created

c.login()

