import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("VK_API_TOKEN")

keyboard_main = "keyboard/keyboard_main.json"
keyboard_pies = "keyboard/keyboard_pies.json"
keyboard_mini_pies = "keyboard/keyboard_mini_pies.json"
keyboard_cookies = "keyboard/keyboard_cookies.json"

KEYBOARD_MESSAGE_BY_STATE = {
    "main_keyboard": [keyboard_main, "Выберите тип выпечки!"],
    "pies_keyboard": [keyboard_pies, "Выберите пирог"],
    "mini_pies_keyboard": [keyboard_mini_pies, "Выберите пирожок"],
    "cookies_keyboard": [keyboard_cookies, "Выберите печенье"],
}

BAKERY = {
    "Шарлотка с яблоками", "Пирог с манкой",
    "Беляши", "Чебурек", "Орешки со сгущенкой",
    "Макаронс",
}


MESSAGE_STATE = {
    "Пироги": "pies_keyboard",
    "Пирожки": "mini_pies_keyboard",
    "Печенье": "cookies_keyboard",
    "Главное меню": "main_keyboard"
}

STATES = [
    "main_keyboard", "pies_keyboard",
    "mini_pies_keyboard", "cookies_keyboard"
]
TRANSITIONS = [
    {"trigger": "main_to_pies", "source": "main_keyboard", "dest": "pies_keyboard"},
    {"trigger": "main_to_mini_pies", "source": "main_keyboard", "dest": "mini_pies_keyboard"},
    {"trigger": "main_to_cookies", "source": "main_keyboard", "dest": "cookies_keyboard"},
    {"trigger": "any_to_main", "source": "*", "dest": "main_keyboard"}
]