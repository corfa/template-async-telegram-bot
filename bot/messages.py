import abc

import telegram as tg
import telegram.ext as tg_ext


class BaseMessages(abc.ABC):
    """
    BaseMessages is an abstract base class for defining messages used by the Telegram bot.

    Methods:
        start: An abstract method that must be implemented by subclasses. It defines the response message
               when the /start command is triggered.
        help: An abstract method that must be implemented by subclasses. It defines the response message
              when the /help command is triggered.
        echo: An abstract method that must be implemented by subclasses. It defines the response message
              when the bot receives any other text message (echo functionality).
    """
    @abc.abstractmethod
    def start(self) -> str:
        """
        An abstract method that must be implemented by subclasses. It defines the response message
        when the /start command is triggered.

        Returns:
            str: The response message for the /start command.
        """
        raise NotImplemented

    @abc.abstractmethod
    def help(self) -> str:
        """
        An abstract method that must be implemented by subclasses. It defines the response message
        when the /help command is triggered.

        Returns:
            str: The response message for the /help command.
        """
        raise NotImplemented

    @abc.abstractmethod
    def echo(self, text: str) -> str:
        """
        An abstract method that must be implemented by subclasses. It defines the response message
        when the bot receives any other text message (echo functionality).

        Args:
            text (str): The input text message received by the bot.

        Returns:
            str: The response message for the echo functionality.
        """
        pass


class RegularUser(BaseMessages):
    def start(self) -> str:
        return 'hello!'

    def help(self) -> str:
        return 'You need to purchase a subscription'

    def echo(self, text: str) -> str:
        return f'{text}'


class PremiumUser(RegularUser):
    def start(self) -> str:
        return 'hello!'

    def help(self) -> str:
        return 'help mock!'


def get_messages(user: tg.User) -> BaseMessages:
    if not user.is_premium:
        return PremiumUser()
    return RegularUser()