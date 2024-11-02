import requests
from requests.auth import HTTPBasicAuth

# Set up the API endpoint
url = "https://api.scale.com/v1/task/5f127f671ab28b001762c204"  # Replace with your task ID

# Headers and authentication using the live API key
headers = {"Accept": "application/json"}
auth = HTTPBasicAuth('live_b1c5a645ea7e418a969b42b134e2d2d6', '')  # Replace 'live_your_api_key' with your actual live API key

# Send GET request to retrieve task details
response = requests.get(url, headers=headers, auth=auth)

# Check for successful response
if response.status_code == 200:
    print("Task Data:", response.json())  # JSON response contains task details and response object
else:
    print("Failed to retrieve task data:", response.status_code, response.text)