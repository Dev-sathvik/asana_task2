from asana.rest import ApiException
from pprint import pprint
from get_initial_sync import fetch_init, fetch_latest
import time
from update_tasks import update_task  # Now accepts a dict
from get_task_names import task_name
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ASANA_PAT")

try:
    # Get initial sync id
    init_sync = fetch_init()
    cur_task_gid = None
    task_gid = ""
    subtask_gid = ""

    # Polling every 10 seconds
    while True:
        time.sleep(10)
        init_sync, data = fetch_latest(init_sync)
        pprint(data)

        for event in data:
            # New subtask added
            if (
                event['action'] == 'added'
                and event.get('parent', {}).get('resource_type') == 'task'
                and event['type'] == 'task'
                and event['resource']['name'] != ""
            ):
                print(event['parent']['name'], event['resource']['name'])
                task_gid = event['parent']['gid']
                subtask_gid = event['resource']['gid']

                start_on_s, due_on_s = task_name(subtask_gid)
                start_on_t, due_on_t = task_name(task_gid)

                print(task_gid, subtask_gid)
                print("Subtask dates:", start_on_s, due_on_s)
                print("Task dates:", start_on_t, due_on_t)

                # Prepare update payload
                update_data = {}

                # If task start_on is None but subtask has it
                if start_on_s is not None and due_on_s is not None:
                    update_data["start_on"] = start_on_s
                    update_data["due_on"] = due_on_s
                    # Asana requires due_on/due_at if start_on is set
                #     if due_on_t is None and due_on_s is not None:
                #         update_data["due_on"] = due_on_s

                # # If task due_on is missing but subtask has it
                # elif due_on_t is None and due_on_s is not None:
                #     update_data["due_on"] = due_on_s

                # Only update if there is something to update
                if update_data:
                    print("Updating main task with:", update_data)
                    update_task(task_gid, update_data)

            # # Handle updates when task's start_on or due_at changes
            # elif (
            #     event['resource']['gid'] == task_gid
            #     and event['action'] != 'deleted'
            #     and event.get('parent') is None
            #     and event['type'] == 'task'
            #     and event['change']['field'] in ['start_on', 'due_at']
            # ):
            #     print("Task date changed:", task_name(task_gid))
            #     # Implement sync logic if needed

except ApiException as e:
    print("Exception when calling EventsApi->get_events: %s\n" % e)
