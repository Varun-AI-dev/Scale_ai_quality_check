import requests
from requests.auth import HTTPBasicAuth
import json
# List of task IDs
task_ids = [
    '5f127f55fdc4150010e37244',  
    '5f127f5ab1cb1300109e4ffc',
    '5f127f5f3a6b100017232099',
    '5f127f643a6b1000172320a5',
    '5f127f671ab28b001762c204',
    '5f127f699740b80017f9b170',
    '5f127f6c3a6b1000172320ad',
    '5f127f6f26831d0010e985e5'

]

# Replace with your live API key
api_key = 'live_b1c5a645ea7e418a969b42b134e2d2d6'

# Initialize an empty list to hold all task data
all_tasks_data = []

# Loop through each task ID and retrieve data
for task_id in task_ids:
    url = f"https://api.scale.com/v1/task/{task_id}"
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(api_key, '')

    # Send GET request to retrieve task details
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        task_data = response.json()  # JSON response contains task details
        all_tasks_data.append(task_data)  # Add task data to the list
    else:
        print(f"Failed to retrieve task data for task ID {task_id}: {response.status_code} {response.text}")

# Save all tasks data to a JSON file
with open("all_tasks_data.json", "w") as json_file:
    json.dump(all_tasks_data, json_file, indent=4)

print("All task data has been saved to 'all_tasks_data.json'.")