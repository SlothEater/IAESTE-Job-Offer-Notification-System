import telegram
import asyncio
import configparser
from src.constants.paths import TELEGRAM_BOT_TOKEN_PATH


async def _send_telegram_bot_message(output_string):
    """
    Sends a message to a Telegram chat using a bot.

    Args:
        output_string (str): The message to be sent.

    Returns:
        None
    """

    # Load bot token and chat ID from configuration file
    config = configparser.ConfigParser()
    config.read(TELEGRAM_BOT_TOKEN_PATH)
    token = config.get('bot_info', 'token').strip("'")
    chat_id = config.get('bot_info', 'chat_id').strip("'")

    # Create bot object using provided token
    bot = telegram.Bot(token=token)

    # Send message to specified chat ID
    await bot.send_message(chat_id=chat_id, text=output_string)


def send_message(output_string):
    """
    Sends a message to a Telegram chat using a bot.

    Args:
        output_string (str): The message to be sent.

    Returns:
        None
    """
    output_string = ("IAESTE platform updates:"
                     f"\n\n{output_string}")
    # Get the event loop and run the message sending coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_telegram_bot_message(output_string))
