from telegram import Message
from telegram.ext import CallbackContext

import resources.Environment as Env
import resources.phrases as phrases
from src.model.Leaderboard import Leaderboard
from src.model.LeaderboardUser import LeaderboardUser
from src.model.User import User
from src.service.bounty_poster_service import reset_bounty_poster_limit
from src.service.bounty_service import reset_bounty, should_reset_bounty
from src.service.crew_service import disband_inactive_crews, warn_inactive_captains
from src.service.leaderboard_service import create_leaderboard, get_leaderboard_rank_message
from src.service.message_service import full_message_send, mention_markdown_v2


def get_leaderboard_message(leaderboard: Leaderboard) -> str:
    """
    Gets the leaderboard message
    :param leaderboard: The leaderboard
    :return: The leaderboard message
    """
    ot_text = phrases.LEADERBOARD_HEADER.format(leaderboard.week, leaderboard.year,
                                                leaderboard.leaderboard_users.count())

    for index, leaderboard_user in enumerate(leaderboard.leaderboard_users):
        leaderboard_user: LeaderboardUser = leaderboard_user
        user: User = User.get_by_id(leaderboard_user.user.id)

        ot_text += '\n'
        ot_text += '\n' if index > 0 else ''
        ot_text += phrases.LEADERBOARD_ROW.format(leaderboard_user.position,
                                                  get_leaderboard_rank_message(leaderboard_user.rank_index),
                                                  mention_markdown_v2(user.tg_user_id, user.tg_first_name),
                                                  user.get_bounty_formatted())

    return ot_text


def manage(context: CallbackContext) -> None:
    """
    Sends the weekly leaderboard to the group
    :param context: Context of callback
    """

    leaderboard = create_leaderboard()

    # Send the leaderboard to the group
    if Env.SEND_MESSAGE_LEADERBOARD.get_bool():
        ot_text = get_leaderboard_message(leaderboard)
        message: Message = full_message_send(context, ot_text, chat_id=Env.OPD_GROUP_ID.get_int())
        message.pin(disable_notification=True)

        # Save the message id
        leaderboard.message_id = message.message_id
        leaderboard.save()

    # Reset bounty poster limit
    reset_bounty_poster_limit(context, reset_previous_leaderboard=True)

    # Reset can join crew flag
    User.update(can_join_crew=True).execute()

    # Reset bounty if last leaderboard of the month
    if should_reset_bounty():
        reset_bounty(context)

    # Disband inactive crews
    disband_inactive_crews(context)

    # Warn captains about inactive crews
    warn_inactive_captains(context)
