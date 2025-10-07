import asana
from asana.rest import ApiException
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv("ASANA_PAT")

def task_name(task_gid):
    configuration = asana.Configuration()
    configuration.access_token = ACCESS_TOKEN
    api_client = asana.ApiClient(configuration)
    tasks_api_instance = asana.TasksApi(api_client)

    opts = {
        'opt_fields': "name,start_on,due_on,due_at"
    }

    try:
        print(f"Fetching task details for ID: {task_gid}")
        api_response = tasks_api_instance.get_task(task_gid, opts)
        print("Task name:", api_response['name'])
        print("Start on:", api_response.get('start_on'))
        print("Due on:", api_response.get('due_on'))
        print("Due at:", api_response.get('due_at'))
        lst = []
        lst.append(api_response['start_on'])
        lst.append(api_response['due_on'])
        return lst
    except ApiException as e:
        print("Exception when calling TasksApi->get_task: %s\n" % e)
