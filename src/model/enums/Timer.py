import resources.Environment as Env


class Timer:
    """
    This class is used to create a timer
    """

    def __init__(self, name: str, cron_expression: str, is_active: bool, should_log: bool, should_run_on_startup: bool,
                 info: str = None):
        """
        Initialize the timer
        :param name: The name of the timer
        :param cron_expression: The cron expression
        :param is_active: Is the timer active
        :param should_log: Should the timer log
        :param should_run_on_startup: Should the timer run once on startup
        """
        self.name = name
        self.cron_expression = cron_expression
        self.is_enabled = is_active
        self.should_log = should_log
        self.should_run_on_startup = should_run_on_startup
        self.info = info


TIMERS: list[Timer] = []
TEMP_DIR_CLEANUP = Timer('temp_dir_cleanup', Env.CRON_TEMP_DIR_CLEANUP.get(),
                         Env.ENABLE_TIMER_TEMP_DIR_CLEANUP.get_bool(), Env.SHOULD_LOG_TIMER_TEMP_DIR_CLEANUP.get_bool(),
                         Env.SHOULD_RUN_ON_STARTUP_TEMP_DIR_CLEANUP.get_bool())
TIMERS.append(TEMP_DIR_CLEANUP)

REDDIT_POST_ONE_PIECE = Timer('reddit_post_one_piece', Env.CRON_REDDIT_POST_ONE_PIECE.get(),
                              Env.ENABLE_TIMER_REDDIT_POST_ONE_PIECE.get_bool(),
                              Env.SHOULD_LOG_TIMER_REDDIT_POST_ONE_PIECE.get_bool(),
                              Env.SHOULD_RUN_ON_STARTUP_REDDIT_POST_ONE_PIECE.get_bool(),
                              info=Env.REDDIT_ONE_PIECE_SUBREDDIT.get())
TIMERS.append(REDDIT_POST_ONE_PIECE)

REDDIT_POST_MEME_PIECE = Timer('reddit_post_meme_piece', Env.CRON_REDDIT_POST_MEME_PIECE.get(),
                               Env.ENABLE_TIMER_REDDIT_POST_MEME_PIECE.get_bool(),
                               Env.SHOULD_LOG_TIMER_REDDIT_POST_MEME_PIECE.get_bool(),
                               Env.SHOULD_RUN_ON_STARTUP_REDDIT_POST_MEME_PIECE.get_bool(),
                               info=Env.REDDIT_MEME_PIECE_SUBREDDIT.get())
TIMERS.append(REDDIT_POST_MEME_PIECE)

TIMER_SEND_LEADERBOARD = Timer('timer_send_leaderboard', Env.CRON_SEND_LEADERBOARD.get(),
                               Env.ENABLE_TIMER_SEND_LEADERBOARD.get_bool(),
                               Env.SHOULD_LOG_TIMER_SEND_LEADERBOARD.get_bool(),
                               Env.SHOULD_RUN_ON_STARTUP_SEND_LEADERBOARD.get_bool())
TIMERS.append(TIMER_SEND_LEADERBOARD)

RESET_BOUNTY_POSTER_LIMIT = Timer('reset_bounty_poster_limit', Env.CRON_RESET_BOUNTY_POSTER_LIMIT.get(),
                                  Env.ENABLE_TIMER_RESET_BOUNTY_POSTER_LIMIT.get_bool(),
                                  Env.SHOULD_LOG_TIMER_RESET_BOUNTY_POSTER_LIMIT.get_bool(),
                                  Env.SHOULD_RUN_ON_STARTUP_RESET_BOUNTY_POSTER_LIMIT.get_bool())
TIMERS.append(RESET_BOUNTY_POSTER_LIMIT)

RESET_CAN_CHANGE_REGION = Timer('reset_can_change_region', Env.CRON_RESET_CAN_CHANGE_REGION.get(),
                                Env.ENABLE_TIMER_RESET_CAN_CHANGE_REGION.get_bool(),
                                Env.SHOULD_LOG_TIMER_RESET_CAN_CHANGE_REGION.get_bool(),
                                Env.SHOULD_RUN_ON_STARTUP_RESET_CAN_CHANGE_REGION.get_bool())
TIMERS.append(RESET_CAN_CHANGE_REGION)

ADD_REGION_BOUNTY_BONUS = Timer('add_region_bounty_bonus', Env.CRON_ADD_REGION_BOUNTY_BONUS.get(),
                                Env.ENABLE_TIMER_ADD_REGION_BOUNTY_BONUS.get_bool(),
                                Env.SHOULD_LOG_TIMER_ADD_REGION_BOUNTY_BONUS.get_bool(),
                                Env.SHOULD_RUN_ON_STARTUP_ADD_REGION_BOUNTY_BONUS.get_bool())
TIMERS.append(ADD_REGION_BOUNTY_BONUS)

ADD_CREW_BOUNTY_BONUS = Timer('add_crew_bounty_bonus', Env.CRON_ADD_CREW_BOUNTY_BONUS.get(),
                              Env.ENABLE_TIMER_ADD_CREW_BOUNTY_BONUS.get_bool(),
                              Env.SHOULD_LOG_TIMER_ADD_CREW_BOUNTY_BONUS.get_bool(),
                              Env.SHOULD_RUN_ON_STARTUP_ADD_CREW_BOUNTY_BONUS.get_bool())
TIMERS.append(ADD_CREW_BOUNTY_BONUS)

ADD_CREW_MVP_BOUNTY_BONUS = Timer('add_crew_mvp_bounty_bonus', Env.CRON_ADD_CREW_MVP_BOUNTY_BONUS.get(),
                                  Env.ENABLE_TIMER_ADD_CREW_MVP_BOUNTY_BONUS.get_bool(),
                                  Env.SHOULD_LOG_TIMER_ADD_CREW_MVP_BOUNTY_BONUS.get_bool(),
                                  Env.SHOULD_RUN_ON_STARTUP_ADD_CREW_MVP_BOUNTY_BONUS.get_bool())
TIMERS.append(ADD_CREW_MVP_BOUNTY_BONUS)

SEND_SCHEDULED_PREDICTIONS = Timer('send_scheduled_predictions', Env.CRON_SEND_SCHEDULED_PREDICTIONS.get(),
                                   Env.ENABLE_TIMER_SEND_SCHEDULED_PREDICTIONS.get_bool(),
                                   Env.SHOULD_LOG_TIMER_SEND_SCHEDULED_PREDICTIONS.get_bool(),
                                   Env.SHOULD_RUN_ON_STARTUP_SEND_SCHEDULED_PREDICTIONS.get_bool())
TIMERS.append(SEND_SCHEDULED_PREDICTIONS)

CLOSE_SCHEDULED_PREDICTIONS = Timer('close_scheduled_predictions', Env.CRON_CLOSE_SCHEDULED_PREDICTIONS.get(),
                                    Env.ENABLE_TIMER_CLOSE_SCHEDULED_PREDICTIONS.get_bool(),
                                    Env.SHOULD_LOG_TIMER_CLOSE_SCHEDULED_PREDICTIONS.get_bool(),
                                    Env.SHOULD_RUN_ON_STARTUP_CLOSE_SCHEDULED_PREDICTIONS.get_bool())
TIMERS.append(CLOSE_SCHEDULED_PREDICTIONS)

SCHEDULE_DEVIL_FRUIT_RELEASE = Timer('schedule_devil_fruit_release', Env.CRON_SCHEDULE_DEVIL_FRUIT_RELEASE.get(),
                                     Env.ENABLE_TIMER_SCHEDULE_DEVIL_FRUIT_RELEASE.get_bool(),
                                     Env.SHOULD_LOG_TIMER_SCHEDULE_DEVIL_FRUIT_RELEASE.get_bool(),
                                     Env.SHOULD_RUN_ON_STARTUP_SCHEDULE_DEVIL_FRUIT_RELEASE.get_bool())
TIMERS.append(SCHEDULE_DEVIL_FRUIT_RELEASE)

RELEASE_SCHEDULED_DEVIL_FRUIT = Timer('release_scheduled_devil_fruit', Env.CRON_RELEASE_SCHEDULED_DEVIL_FRUIT.get(),
                                      Env.ENABLE_TIMER_RELEASE_SCHEDULED_DEVIL_FRUIT.get_bool(),
                                      Env.SHOULD_LOG_TIMER_RELEASE_SCHEDULED_DEVIL_FRUIT.get_bool(),
                                      Env.SHOULD_RUN_ON_STARTUP_RELEASE_SCHEDULED_DEVIL_FRUIT.get_bool())
TIMERS.append(RELEASE_SCHEDULED_DEVIL_FRUIT)

RESPAWN_DEVIL_FRUIT = Timer('respawn_devil_fruit', Env.CRON_RESPAWN_DEVIL_FRUIT.get(),
                            Env.ENABLE_TIMER_RESPAWN_DEVIL_FRUIT.get_bool(),
                            Env.SHOULD_LOG_TIMER_RESPAWN_DEVIL_FRUIT.get_bool(),
                            Env.SHOULD_RUN_ON_STARTUP_RESPAWN_DEVIL_FRUIT.get_bool())
TIMERS.append(RESPAWN_DEVIL_FRUIT)
