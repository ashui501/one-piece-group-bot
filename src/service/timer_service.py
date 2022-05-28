import logging

from apscheduler.triggers.cron import CronTrigger
from telegram.ext import CallbackContext, Dispatcher, Job

import src.model.enums.Timer as Timer
from src.chat.group.screens.screen_doc_q_game import reset_playability as reset_doc_q_game
from src.chat.group.screens.screen_leaderboard import manage as send_leaderboard
from src.chat.group.screens.screen_reddit_post import manage as send_reddit_post
from src.chat.manage_message import init, end
from src.service.bounty_poster_service import reset_bounty_poster_limit
from src.service.bounty_service import add_region_bounty
from src.service.download_service import cleanup_temp_dir
from src.service.location_service import reset_can_change_region


def add_to_context(context: CallbackContext, timer: Timer.Timer) -> Job:
    """
    Add a job to the context
    :param context: The context
    :param timer: The timer
    :rtype: Job
    """
    job = context.job_queue.run_custom(
        callback=run,
        job_kwargs={"trigger": CronTrigger.from_crontab(timer.cron_expression)},
        name=timer.name,
        context=timer
    )
    logging.info(f'Next run of "{timer.name}" is {job.next_run_time}')
    return job


def set_timers(dispatcher: Dispatcher) -> None:
    """
    Set the timers
    :param dispatcher: The dispatcher
    :type dispatcher: Dispatcher
    :return: None
    :rtype: None
    """

    context = CallbackContext(dispatcher)

    # Temp folder cleanup timer
    add_to_context(context, Timer.TEMP_DIR_CLEANUP)

    # Reddit post One Piece
    add_to_context(context, Timer.REDDIT_POST_ONE_PIECE)

    # Reddit post Meme Piece
    add_to_context(context, Timer.REDDIT_POST_MEME_PIECE)

    # Leaderboard timer
    add_to_context(context, Timer.TIMER_SEND_LEADERBOARD)

    # Reset Doc Q Game timer
    add_to_context(context, Timer.RESET_DOC_Q_GAME)

    # Reset bounty poster limit
    add_to_context(context, Timer.RESET_BOUNTY_POSTER_LIMIT)

    # Reset can change region
    add_to_context(context, Timer.RESET_CAN_CHANGE_REGION)

    # Increment bounty by region
    add_to_context(context, Timer.ADD_REGION_BOUNTY)


def run(context: CallbackContext) -> None:
    """
    Run the timers
    :param context: The context
    :return: None
    """

    job = context.job
    if not isinstance(job.context, Timer.Timer):
        logging.error(f'Job {job.name} context is not a Timer')
        return

    timer: Timer.Timer = job.context
    if not timer.is_enabled:
        logging.info(f'Skipping timer {job.name}')
        return

    db = init()
    logging.info(f'Running timer {context.job.name}')

    match timer:
        case Timer.REDDIT_POST_ONE_PIECE | Timer.REDDIT_POST_MEME_PIECE:
            send_reddit_post(context, timer.info)
        case Timer.TEMP_DIR_CLEANUP:
            cleanup_temp_dir()
        case Timer.TIMER_SEND_LEADERBOARD:
            send_leaderboard(context)
        case Timer.RESET_DOC_Q_GAME:
            reset_doc_q_game(context)
        case Timer.RESET_BOUNTY_POSTER_LIMIT:
            reset_bounty_poster_limit(context)
        case Timer.RESET_CAN_CHANGE_REGION:
            reset_can_change_region(context)
        case Timer.ADD_REGION_BOUNTY:
            add_region_bounty(context)
        case _:
            logging.error(f'Unknown timer {job.name}')

    logging.info(f'Finished timer {context.job.name}')
    end(db)

    return