import datetime

from peewee import *

from src.model.BaseModel import BaseModel
from src.model.GroupChat import GroupChat
from src.model.User import User
from src.model.enums.GameStatus import GameStatus
from src.model.enums.SavedMediaName import SavedMediaName
from src.model.game.GameDifficulty import GameDifficulty
from src.model.game.GameType import GameType


class Game(BaseModel):
    """
    Game class
    """
    id = PrimaryKeyField()
    challenger = ForeignKeyField(User, backref='game_challengers', on_delete='CASCADE',
                                 on_update='CASCADE')
    opponent = ForeignKeyField(User, backref='game_opponents', on_delete='CASCADE', on_update='CASCADE')
    type = SmallIntegerField(null=True)
    board = CharField(max_length=9999, null=True)
    date = DateTimeField(default=datetime.datetime.now)
    status = SmallIntegerField(default=GameStatus.AWAITING_SELECTION)
    group_chat = ForeignKeyField(GroupChat, null=True, backref='game_groups_chats', on_delete='RESTRICT',
                                 on_update='CASCADE')
    message_id = IntegerField(null=True)
    wager = IntegerField(null=True)

    class Meta:
        db_table = 'game'

    def is_player(self, user: User) -> bool:
        """
        Check if the user is a player of the game
        :param user: The user
        :return: True if the user is a player, False otherwise
        """

        return self.challenger == user or self.opponent == user

    def get_saved_media_name(self) -> SavedMediaName:
        """
        Get the SavedMediaName for this GameType
        :return: The SavedMediaName
        """
        return GameType(self.type).get_saved_media_name()

    def get_difficulty(self) -> GameDifficulty:
        """
        Get the difficulty level of the game
        :return: The difficulty level
        """

        return GameDifficulty.get_from_total_wager(int(str(self.wager)))


Game.create_table()
