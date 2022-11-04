import datetime

import src.model.enums.LeaderboardRank as LeaderboardRank
from src.model.Leaderboard import Leaderboard
from src.model.LeaderboardUser import LeaderboardUser
from src.model.User import User
from src.model.enums.Location import get_first_new_world, get_last_paradise


def create_leaderboard() -> Leaderboard:
    """
    Creates a leaderboard list
    :return: The leaderboard
    """

    year = datetime.datetime.now().isocalendar()[0]
    week = datetime.datetime.now().isocalendar()[1]

    # Delete the leaderboard if it exists
    Leaderboard.delete().where(Leaderboard.year == year, Leaderboard.week == week).execute()

    # Create a leaderboard for the current week and year
    leaderboard = Leaderboard()
    leaderboard.year = datetime.datetime.now().isocalendar()[0]
    leaderboard.week = datetime.datetime.now().isocalendar()[1]
    leaderboard.save()

    # Create the leaderboard users
    create_leaderboard_users(leaderboard)

    return leaderboard


def get_leaderboard_rank_message(index: int) -> str:
    """
    Gets the rank message of a leaderboard rank
    :param index: The leaderboard rank index
    :return: The leaderboard rank message
    """
    leaderboard_rank: LeaderboardRank = LeaderboardRank.get_rank_by_index(index)
    return leaderboard_rank.get_emoji_and_rank_message()


def create_leaderboard_users(leaderboard: Leaderboard) -> list[LeaderboardUser]:
    """
    Creates a leaderboard list
    :param leaderboard: The leaderboard to create the users for
    :return: The leaderboard users
    """

    leaderboard_users: list[LeaderboardUser] = []
    position = 1

    # Get previous leaderboard users who were Emperors or higher
    previous_leaderboard_users: list[LeaderboardUser] = get_leaderboard(1).leaderboard_users

    # Eligible users for Pirate King position - Those who were Emperor or higher in the previous leaderboard
    eligible_pk_users: list[User] = [leaderboard_user.user for leaderboard_user in previous_leaderboard_users
                                     if leaderboard_user.rank_index <= LeaderboardRank.EMPEROR.index]

    # Get current New World users
    new_world_users: list[User] = list(User.select()
                                       .where((User.location_level >= get_first_new_world().level)
                                              & (User.get_is_not_arrested_statement_condition()))
                                       .order_by(User.bounty.desc()))

    # Save Pirate King, if available
    for user in new_world_users:
        if user in eligible_pk_users:
            leaderboard_user: LeaderboardUser = save_leaderboard_user(leaderboard, user, position,
                                                                      LeaderboardRank.PIRATE_KING)
            leaderboard_users.append(leaderboard_user)
            break

    # Save Emperors, next 4 users
    for index, user in enumerate(new_world_users):
        if not any(lu for lu in leaderboard_users if lu.user == user):
            leaderboard_user: LeaderboardUser = save_leaderboard_user(leaderboard, user, position,
                                                                      LeaderboardRank.EMPEROR)
            leaderboard_users.append(leaderboard_user)
            position += 1
            if index == 3:
                break

    # Save First Mates, next 4 users
    for index, user in enumerate(new_world_users):
        if not any(lu for lu in leaderboard_users if lu.user == user):
            leaderboard_user: LeaderboardUser = save_leaderboard_user(leaderboard, user, position,
                                                                      LeaderboardRank.FIRST_MATE)
            leaderboard_users.append(leaderboard_user)
            position += 1
            if index == 3:
                break

    # Get current Paradise users
    paradise_users: list[User] = list(User.select()
                                      .where((User.location_level <= get_last_paradise().level)
                                             & (User.get_is_not_arrested_statement_condition()))
                                      .order_by(User.bounty.desc()))

    # Save Supernovas, next 11 users
    for index, user in enumerate(paradise_users):
        if not any(lu for lu in leaderboard_users if lu.user == user):
            leaderboard_user: LeaderboardUser = save_leaderboard_user(leaderboard, user, position,
                                                                      LeaderboardRank.SUPERNOVA)
            leaderboard_users.append(leaderboard_user)
            position += 1
            if index == 10:
                break

    return leaderboard_users


def save_leaderboard_user(leaderboard: Leaderboard, user: User, position: int, rank: LeaderboardRank.LeaderboardRank
                          ) -> LeaderboardUser:
    """
    Saves a leaderboard user
    :param leaderboard: The leaderboard
    :param user: The user
    :param position: The position
    :param rank: The rank
    """
    leaderboard_user = LeaderboardUser()
    leaderboard_user.leaderboard = leaderboard
    leaderboard_user.user = user
    leaderboard_user.position = position
    leaderboard_user.rank_index = rank.index
    leaderboard_user.save()

    return leaderboard_user


def get_leaderboard(index: int = 0) -> Leaderboard | None:
    """
    Gets the current leaderboard
    :param index: The index of the leaderboard to get. Higher the index, older the leaderboard.
    :return: The leaderboard
    """
    leaderboard: Leaderboard = (Leaderboard.select()
                                .order_by(Leaderboard.year.desc(),
                                          Leaderboard.week.desc())
                                .limit(1)
                                .offset(index)
                                .first())
    return leaderboard


def get_leaderboard_user(user: User, leaderboard: Leaderboard = None, index: int = None) -> LeaderboardUser | None:
    """
    Gets the leaderboard user for the user
    :param user: The user to get the leaderboard user for
    :param leaderboard: The leaderboard to get the leaderboard user for
    :param index: The index of the leaderboard to get. Higher the index, older the leaderboard
    :return: The leaderboard user
    """

    if leaderboard is None and index is None:
        raise ValueError("Either leaderboard or index must be provided")

    if leaderboard is None:
        leaderboard = get_leaderboard(index)

    leaderboard_user: LeaderboardUser = leaderboard.leaderboard_users.where(LeaderboardUser.user == user).first()
    return leaderboard_user


def get_current_leaderboard_user(user: User) -> LeaderboardUser | None:
    """
    Gets the current leaderboard user for the user
    :param user: The user to get the leaderboard user for
    :return: The leaderboard user
    """

    return get_leaderboard_user(user, index=0)


def get_current_leaderboard_rank(user: User) -> LeaderboardRank.LeaderboardRank:
    """
    Gets the current leaderboard rank for the user
    :param user: The user to get the leaderboard rank for
    :return: The leaderboard rank
    """

    leaderboard_user: LeaderboardUser = get_current_leaderboard_user(user)
    return LeaderboardRank.get_rank_by_leaderboard_user(leaderboard_user)
