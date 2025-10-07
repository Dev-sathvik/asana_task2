import asana
from asana.rest import ApiException
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN = os.getenv("ASANA_PAT")

#update the new task name preceeded with project name
def update_task(task_name, task_id):
        configuration = asana.Configuration()
        configuration.access_token = ACCESS_TOKEN
        api_client = asana.ApiClient(configuration)

        # create an instance of the API class
        tasks_api_instance = asana.TasksApi(api_client)
        body = {"data": {"name": f"{task_name}"}} # dict | The task to update.
        task_gid = f"{task_id}" # str | The task to operate on.
        opts = {
            'opt_fields': "actual_time_minutes" # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
        }

        try:
            # Update a task
            api_response = tasks_api_instance.update_task(body, task_gid, opts)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling TasksApi->update_task: %s\n" % e)