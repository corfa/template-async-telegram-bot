import os
import telegram.ext as tg_ext
from dotenv import load_dotenv

from bot import handlers

load_dotenv()

def main() -> None:
    telegram_token = os.getenv('TOKEN', '')
    application = tg_ext.Application.builder().token(telegram_token).build()

    handlers.setup_handlers(application)

    application.run_polling()


if __name__ == "__main__":
    main()