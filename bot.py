import logging
import os
import time
from collections import defaultdict

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkEventType, VkLongPoll

from config import configure_logging
from constant import BAKERY, KEYBOARD_MESSAGE_BY_STATE, TOKEN
from db import DB_BakeryProducts
from keyboard import create_keyboard


def send_message(sender, keyboard_path, message):
    """Функция для отправки личных сообщений с кнопками."""

    for i in range(0, 3):
        try:
            with open(keyboard_path, 'r', encoding='UTF-8') as keyboard:

                vk.messages.send(
                    user_id=sender,
                    random_id=0,
                    keyboard=keyboard.read(),
                    message=message)
        except:
            logging.exception(
                f'Ошибка отправки сообщения пользователю с id {sender}'
            )
            time.sleep(0.5)
            continue
        break


def take_path_bakery(product_name):
    try:
        db = DB_BakeryProducts()
        descr, path = db.get_cake_descr_path(product_name)
        return descr, path
    except Exception:
        logging.exception(f'Ошибка соединения c базой')


def send_message_bakery(sender, message):
    for i in range(0, 3):
        try:
            descr, path = take_path_bakery(message)
            photo = upload.photo_messages(path)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            vk.messages.send(
                peer_id=sender,
                random_id=0,
                message=descr,
                attachment=attachment)
        except:
            logging.exception(
                f'Ошибка отправки сообщения пользователю с id {sender}'
            )
            time.sleep(0.2)
            continue
        break


def message_process(sender, message, keyboard):
    keyboard.click(message, sender)
    if message in BAKERY:
        send_message_bakery(sender, message)
    keyboard_path, message = KEYBOARD_MESSAGE_BY_STATE[keyboard.state]
    send_message(sender, keyboard_path, message)


if __name__ == "__main__":
    configure_logging()
    authorize = vk_api.VkApi(token=TOKEN)
    vk = authorize.get_api()
    upload = VkUpload(vk)
    longpool = VkLongPoll(authorize)
    logging.info("Запуск бота!")
    user_state = defaultdict(create_keyboard)
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = event.text
            sender = event.user_id
            keyboard = user_state[sender]
            try:
                message_process(sender, message, keyboard)
            except:
                logging.exception('Ошибка во время отправки сообщения')
