import asana
from asana.rest import ApiException
import os
from dotenv import load_dotenv
from pprint import pprint

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("ASANA_PAT")


def update_task(task_gid, update_fields: dict):
    """
    Update fields of a task in Asana.

    Args:
        task_gid (str): The GID of the task to update.
        update_fields (dict): Dictionary of fields to update, e.g.,
                              {"start_on": "2025-10-10", "due_on": "2025-10-15"}
    """
    # Set up configuration
    configuration = asana.Configuration()
    configuration.access_token = ACCESS_TOKEN
    api_client = asana.ApiClient(configuration)

    tasks_api_instance = asana.TasksApi(api_client)
    body = {"data": update_fields}  # Send all fields together

    # Optional fields to include in response
    opts = {
        #'opt_fields': "gid,name,notes,start_on,due_on,due_at,assignee,completed"
    }

    try:
        api_response = tasks_api_instance.update_task(body, task_gid, opts)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->update_task: %s\n" % e)


# Example usage:
# update_task("1234567890", {"start_on": "2025-10-10", "due_on": "2025-10-15"})
