import logging
import os

from telegram import Update
from telegram.ext import CallbackContext

import constants as c
from src.chat.admin.admin_chat_manager import manage as manage_admin_chat
from src.chat.group.group_chat_manager import manage as manage_group_chat
from src.chat.private.private_chat_manager import manage as manage_private_chat


def manage(update: Update, context: CallbackContext) -> None:
    """
    Manage the callback query
    :param update: The update
    :param context: The context
    :return: None
    """

    # Filter by chat id
    try:
        chat_id = update.callback_query.message.chat_id

        # Private chat
        if chat_id == update.callback_query.from_user.id:
            manage_private_chat(update, context)

        # Group chat
        if chat_id == int(os.environ[c.ENV_OPD_GROUP_ID]):
            manage_group_chat(update, context)

        # Admin chat
        if chat_id == int(os.environ[c.ENV_ADMIN_GROUP_ID]):
            manage_admin_chat(update, context)

        update.callback_query.answer()
    except Exception as e:
        logging.error(f'Error in manage callback query: {e}')
        raise e
