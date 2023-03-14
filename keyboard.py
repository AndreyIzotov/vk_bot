import logging

from transitions import Machine, MachineError

from constant import MESSAGE_STATE, STATES, TRANSITIONS


class Matter(object):

    def click(self, message, user_id):

        STATE_KEYBOARD = {
            "Пироги": self.main_to_pies,
            "Пирожки": self.main_to_mini_pies,
            "Печенье": self.main_to_cookies,
            "Главное меню": self.any_to_main
        }
        click = STATE_KEYBOARD.get(message)
        if click is not None:
            try:
                click()

            except MachineError:
                logging.exception(f"Переход невозможен из {self.state}  "
                                  f"в {MESSAGE_STATE.get(message,)} для пользователя с id {user_id}")


def create_keyboard():
    keyboard = Matter()
    Machine(keyboard, states=STATES, transitions=TRANSITIONS, initial="main_keyboard")

    return keyboard
