import abc
import typing as tp

import telegram as tg
import telegram.ext as tg_ext

from bot import messages


class BaseHandler(abc.ABC):
    """
    BaseHandler is an abstract base class for defining Telegram bot message handlers.

    Attributes:
        user (Optional[tg.User]): The Telegram user associated with the update. It will be set when the handler is called.
        messages (Dict[str, str]): A dictionary containing messages specific to the user. It will be populated using `messages.get_messages()`.

    Methods:
        __call__: This method is called when an update is received. It sets the `user` attribute, retrieves user-specific messages, and calls the `handle` method.
        handle: An abstract method that must be implemented by subclasses. It defines the behavior of the handler for processing updates.
    """

    def __init__(self) -> None:
        """
        Initializes a new BaseHandler instance.
        """
        self.user: tp.Optional[tg.User] = None

    async def __call__(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Invoked when an update is received. Sets the `user` attribute, retrieves user-specific messages,
        and calls the `handle` method for further processing.

        Args:
            update (tg.Update): The Telegram update received from the bot.
            context (tg_ext.ContextTypes.DEFAULT_TYPE): The context associated with the update.

        Returns:
            None
        """
        self.user = update.effective_user
        self.messages = messages.get_messages(self.user)
        await self.handle(update, context)

    @abc.abstractmethod
    async def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        An abstract method that must be implemented by subclasses. This method defines the behavior of the handler
        for processing updates based on the received update and context.

        Args:
            update (tg.Update): The Telegram update received from the bot.
            context (tg_ext.ContextTypes.DEFAULT_TYPE): The context associated with the update.
            
        Returns:
            None
        """
        raise NotImplemented


class StartHandler(BaseHandler):
    async def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_text(self.messages.start())


class HelpHandler(BaseHandler):
    async def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_text(self.messages.help())


class EchoHandler(BaseHandler):
    async def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_text(
            self.messages.echo(update.message.text)
        )


def setup_handlers(application: tg_ext.Application) -> None:
    application.add_handler(tg_ext.CommandHandler('start', StartHandler()))
    application.add_handler(tg_ext.CommandHandler('help', HelpHandler()))

    application.add_handler(
        tg_ext.MessageHandler(
            tg_ext.filters.TEXT & ~tg_ext.filters.COMMAND, EchoHandler()
        )
    )