import requests
import pandas as pd
from datetime import datetime
import os

# set the URL for the station status JSON feed
url = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json'

# make a request to the URL and get the JSON response
response = requests.get(url).json()

# get the current date and time
now = datetime.utcnow()

# round the time to the nearest quarter hour
minute = now.minute // 15 * 15
now = now.replace(minute=minute)

# add a column for the current date and time
for obj in response['data']['stations']:
    obj['last_update'] = now

# convert the JSON response to a DataFrame
df = pd.DataFrame(response['data']['stations'])

# create a filename with the current date
filename = 'station_data_' + now.strftime('%Y-%m-%d') + '.csv'

# check if the file exists
if os.path.exists(filename):
    # if the file exists, append the data to it
    df.to_csv(filename, mode='a', header=False)
else:
    # if the file doesn't exist, create a new file and write the data to it
    df.to_csv(filename, mode='w', header=True)
