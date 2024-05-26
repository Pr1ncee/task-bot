from core.base_enum import BaseEnum


class Transitions(BaseEnum):
    START = {'trigger': 'start', 'source': 'START', 'dest': 'GET_NAME'}
    GET_NAME = {'trigger': 'get_name', 'source': 'GET_NAME', 'dest': 'GET_USERNAME'}
    GET_USERNAME = {'trigger': 'get_username', 'source': 'GET_USERNAME', 'dest': 'START'}
    CREATE_TASK = {'trigger': 'create_task', 'source': ['START', 'GET_USERNAME'], 'dest': 'GET_TASK_TITLE'}
    GET_TASK_TITLE = {'trigger': 'get_task_title', 'source': 'GET_TASK_TITLE', 'dest': 'GET_TASK_DESCRIPTION'}
    GET_TASK_DESCRIPTION = {'trigger': 'get_task_description', 'source': 'GET_TASK_DESCRIPTION', 'dest': 'START'}
    MARK_TASK_COMPLETED = {'trigger': "mark_task_completed", 'source': 'MARK_TASK_COMPLETED', 'dest': 'START'}
    DELETE_TASK = {'trigger': "delete_task", "source": "DELETE_TASK", 'dest': "START"}
    CANCEL = {'trigger': 'cancel', 'source': '*', 'dest': 'START'}
