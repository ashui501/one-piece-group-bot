from telegram import Update
from telegram.ext import CallbackContext

import resources.Environment as Env
import resources.phrases as phrases
from src.model.Prediction import Prediction
from src.model.PredictionOption import PredictionOption
from src.model.PredictionOptionUser import PredictionOptionUser
from src.model.User import User
from src.model.enums.Command import Command
from src.model.enums.PredictionStatus import PredictionStatus
from src.service.bounty_service import get_wager_amount, validate_wager
from src.service.message_service import full_message_send
from src.service.prediction_service import refresh


def validate(update: Update, context: CallbackContext, user: User, command: Command) -> tuple[Prediction,
                                                                                              PredictionOption, int,
                                                                                              int] | tuple[None, None,
                                                                                                           None, None]:
    """
    Validate the prediction bet
    :param update: The update object
    :param context: The context object
    :param user: The user object
    :param command: The command
    :return: None if validation failed or (prediction, prediction_option, wager, option number) if validation succeeded
    """

    error_tuple = None, None, None, None

    if len(command.parameters) != 2:
        full_message_send(context, phrases.PREDICTION_BET_INVALID_FORMAT, update=update, add_delete_button=True)
        return error_tuple

    # Wager basic validation, error message is sent by validate_wager
    if not validate_wager(update, context, user, command.parameters[0], Env.PREDICTION_BET_MIN_WAGER.get_int()):
        return error_tuple

    # Get prediction from message id
    prediction: Prediction = Prediction.get_or_none(Prediction.message_id == update.message.reply_to_message.message_id)
    if prediction is None:
        full_message_send(context, phrases.PREDICTION_NOT_FOUND_IN_REPLY, update=update)
        return error_tuple

    # Prediction is not open
    if PredictionStatus(prediction.status) is not PredictionStatus.SENT:
        full_message_send(context, phrases.PREDICTION_CLOSED_FOR_BETS, update=update)
        return error_tuple

    prediction_options: list[PredictionOption] = prediction.prediction_options

    # User has already bet and prediction does not allow multiple bets
    prediction_options_user: list[PredictionOptionUser] = PredictionOptionUser.select().where(
        (PredictionOptionUser.prediction_option.in_(prediction_options))
        & (PredictionOptionUser.user == user))
    if len(prediction_options_user) > 0 and prediction.allow_multiple_choices is False:
        full_message_send(context, phrases.PREDICTION_ALREADY_BET, update=update)
        return error_tuple

    # Option is not valid
    prediction_option = [prediction_option for prediction_option in prediction_options if
                         prediction_option.number == int(command.parameters[1])]
    if len(prediction_option) == 0:
        full_message_send(context, phrases.PREDICTION_OPTION_NOT_FOUND.format(command.parameters[1]), update=update)
        return error_tuple

    return prediction, prediction_option[0], get_wager_amount(command.parameters[0]), int(command.parameters[1])


def manage(update: Update, context: CallbackContext, user: User, command: Command) -> None:
    """
    Manage the change region request
    :param update: The update object
    :param context: The context object
    :param user: The user object
    :param command: The command
    :return: None
    """
    validation_tuple = validate(update, context, user, command)

    # Need single assignment to enable IDE type detection
    prediction: Prediction = validation_tuple[0]
    prediction_option: PredictionOption = validation_tuple[1]
    wager: int = validation_tuple[2]
    option_number: int = validation_tuple[3]

    if prediction is None or prediction_option is None or wager is None or option_number is None:
        return

    # Add prediction option user
    prediction_option_user = PredictionOptionUser()
    prediction_option_user.prediction_option = prediction_option
    prediction_option_user.user = user
    prediction_option_user.wager = wager
    prediction_option_user.save()

    # Remove wager from user balance
    user.bounty -= wager
    user.pending_bounty += wager
    user.save()

    # Send success message
    full_message_send(context, phrases.PREDICTION_BET_SUCCESS, update=update, add_delete_button=True)

    # Update prediction text
    refresh(context, prediction)