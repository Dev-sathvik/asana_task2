
from asana.rest import ApiException
from pprint import pprint
from get_initial_sync import fetch_init, fetch_latest
import time
from update_tasks import update_task
from get_task_name import task_name
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ASANA_PAT")
#print(ACCESS_TOKEN)

try:
    # Get initial sync id
    init_sync = fetch_init()
    cur_task_gid = None
    final_task_name = ""
    parent_name = ""
    # polling every 10 seconds
    while True:
        time.sleep(10)
        init_sync, data = fetch_latest(init_sync)
        pprint(data)
        for event in data:
            # if new task is add, then remember the task id and parent project
            if event['action'] == 'added' and event['parent']['resource_type'] == 'project' and event['resource']['name'] != "":
                print(event['parent']['name'], event['resource']['name'])
                # final_task_name = event['resource']['name']
                cur_task_gid = event['resource']['gid']
                parent_name = event['parent']['name']
                # update task name when task name changes 
            elif event['action'] != 'deleted' and event['resource']['gid'] == cur_task_gid:
                cur_name = task_name(cur_task_gid)
                if not cur_name.startswith(parent_name):
                    print("Task name: ", cur_name)
                    newtask_name = parent_name + " - " + cur_name
                    update_task(newtask_name, cur_task_gid)
                break

except ApiException as e:
    print("Exception when calling EventsApi->get_events: %s\n" % e)