from core.fsm.state_machine import StateMachine


def get_user_state(user_id: int, local_state: dict) -> StateMachine:
    """
    Функция-утилита для получение текущего состояния пользователя в Конечном Автомате.
    :param user_id: уникальный ID пользователя в Telegram
    :param local_state: локальное хранилище состояний в Конечном Автомате
    :return: объект Машины для определенного пользователя
    """
    if user_id not in local_state:
        local_state[user_id] = StateMachine()
    return local_state[user_id]
