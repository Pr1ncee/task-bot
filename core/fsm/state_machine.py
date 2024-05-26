from transitions import Machine

from core.fsm.states import States
from core.fsm.transitions import Transitions


class StateMachine(Machine):
    """
    Класс, который хранит состояния, переходы и модели.
    Наследует класс Machine из библиотеки transitions.
    """
    def __init__(self):
        """
        Функция инициализирует некоторые переменные, которые будут сохранены в процессе работы программы,
        а также передает в родительский класс объявленных переходов и состояний.
        """
        self.user_name = None
        self.task_title = None
        super().__init__(
            states=States.values(),
            transitions=Transitions.values(),
            initial=States.START.value
        )
