import requests
import csv
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# 20240225
def login(url):
    load_dotenv()
    # Define the username and password
    post_data = {
        'username': os.environ.get('VIZHUB_LOGIN'), 
        'password': os.environ.get('VIZHUB_PW') 
    }

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Send the POST request
    # response = requests.post(url, data=data)
    response = requests.post(url, headers=headers, data=json.dumps(post_data))

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from ThingsBoard API. Status code:", response.status_code)
        return None


def fetch_sensor_data(device_id, sensor_key, start_ts, end_ts, access_token):
    url = f'http://locationai.tech:8080/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys={sensor_key}'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Authorization': f'Bearer {access_token}'
    }
    params = {
        'startTs': start_ts,
        'endTs': end_ts
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from ThingsBoard API. Status code:", response.status_code)
        return None

def timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":

    url = f'http://locationai.tech:8080/api/auth/login'

    response_data = login(url)

    access_token = response_data['token']
    # access_token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsb2NhdGlvbmFpYWRtaW5AbG9jYXRpb25haS5jb20iLCJzY29wZXMiOlsiQ1VTVE9NRVJfVVNFUiJdLCJ1c2VySWQiOiJlZDE0Yjk1MC1lODc4LTExZWItYjUwNy1lMTZkMWM3MTExOTUiLCJmaXJzdE5hbWUiOiJhZG1pbiIsImxhc3ROYW1lIjoibG9jYXRpb25haSIsImVuYWJsZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiJiMDQ1YTBjMC04ZGYxLTExZWItOWUyYS0wMWU3YjhiZmI0ZDkiLCJjdXN0b21lcklkIjoiYzU4Y2EyNDAtZTQ4YS0xMWViLWI1MDctZTE2ZDFjNzExMTk1IiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDg3MzkzMzgsImV4cCI6MTcwODc0ODMzOH0.c3PmrwNSSPUAHd5GfNMcaRv7d6vKk_k_Doj384lcVi_F0T7yvLgQb6pvQZxn2pz9jGkgprnKQ1E2YOYu9S-3Qg'

    device_id = '58366820-ae63-11ee-a39c-0f270afb2199' #STEM2
    
    # sensor_key = input("Enter sensor key (e.g., CO2): ")
    # start_ts = input("Enter start timestamp (in milliseconds): ")
    # end_ts = input("Enter end timestamp (in milliseconds): ")
    sensor_key = "CO2"
    start_ts = 1700000000000
    end_ts = 1710000000000

    data = fetch_sensor_data(device_id, sensor_key, start_ts, end_ts, access_token)
    if data and sensor_key in data:
        timestamps = [entry['ts'] for entry in data[sensor_key]]
        values = [entry['value'] for entry in data[sensor_key]]

        # Convert timestamps to datetime strings
        timestamps = [timestamp_to_datetime(ts) for ts in timestamps]

        with open(f'csv_data/thingsboard_{sensor_key.lower()}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', sensor_key])
            writer.writerows(zip(timestamps, values))

        print(f"Data written to thingsboard_{sensor_key.lower()}_data.csv")
    else:
        print(f"No data available for the specified sensor ({sensor_key}) or time range.")